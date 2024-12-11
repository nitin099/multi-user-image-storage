import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from django.http import HttpResponse, FileResponse
from .models import Image
from .serializers import ImageSerializer
from django.shortcuts import get_object_or_404
from django.conf import settings


class UploadImageView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES['file']
        metadata = request.data.get('metadata', {})
        file_name = file.name
        s3_key = f"images/{file_name}"

        # Save the file to S3
        saved_path = default_storage.save(s3_key, file)

        # Store metadata and S3 path in the database
        image = Image.objects.create(file_name=file_name, s3_key=s3_key, metadata=metadata)

        return Response({
            "message": "Image uploaded successfully!",
            "id": image.id,
            "s3_path": saved_path
        }, status=status.HTTP_201_CREATED)

class ListImagesView(APIView):
    def get(self, request):
        filter_key1 = request.GET.get('key1')
        filter_value1 = request.GET.get('value1')
        filter_key2 = request.GET.get('key2')
        filter_value2 = request.GET.get('value2')

        images = Image.objects.all()
        if filter_key1 and filter_value1:
            images = images.filter(metadata__contains={filter_key1: filter_value1})
        if filter_key2 and filter_value2:
            images = images.filter(metadata__contains={filter_key2: filter_value2})

        data = [{"id": img.id, "file_name": img.file_name, "metadata": img.metadata, "s3_key": img.s3_key} for img in images]
        return Response(data, status=status.HTTP_200_OK)

class ViewImageView(APIView):
    def get(self, request, image_id):
        try:
            image = Image.objects.get(id=image_id)
            s3 = boto3.client(
                's3',
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
            )
            url = s3.generate_presigned_url(
                'get_object',
                Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': image.s3_key},
                ExpiresIn=3600  # URL valid for 1 hour
            )
            return Response({"url": url}, status=status.HTTP_200_OK)
        except Image.DoesNotExist:
            return Response({"error": "Image not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteImageView(APIView):
    def delete(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
