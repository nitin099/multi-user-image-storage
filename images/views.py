from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.http import HttpResponse, FileResponse
from .models import Image
from .serializers import ImageSerializer
from django.shortcuts import get_object_or_404

class UploadImageView(APIView):
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListImagesView(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        import pdb; pdb.set_trace()
        queryset = Image.objects.all()
        metadata_key = self.request.query_params.get('metadata_key')
        metadata_value = self.request.query_params.get('metadata_value')
        if metadata_key and metadata_value:
            queryset = queryset.filter(metadata__contains={metadata_key: metadata_value})
        return queryset

class ImageView(APIView):
    def get(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        response_type = request.query_params.get('type', 'view')
        if response_type == 'download':
            return FileResponse(image.image, as_attachment=True)
        return FileResponse(image.image)

class DeleteImageView(APIView):
    def delete(self, request, pk):
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
