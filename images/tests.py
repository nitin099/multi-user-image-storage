from moto import mock_s3
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Image
from django.core.files.uploadedfile import SimpleUploadedFile
import boto3

class ImageAPITest(TestCase):
    @mock_s3
    def setUp(self):
        self.client = APIClient()
        self.s3 = boto3.client(
            's3',
            aws_access_key_id='test',
            aws_secret_access_key='test',
            endpoint_url='http://localhost:4566'
        )
        self.bucket_name = 'localstack-bucket'
        self.s3.create_bucket(Bucket=self.bucket_name)
        self.image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        self.image_obj = Image.objects.create(image=self.image, metadata={"tag": "test"})

    def test_upload_image(self):
        response = self.client.post('/api/images/upload/', {
            "image": self.image,
            "metadata": {"tag": "test"}
        }, format='multipart')
        self.assertEqual(response.status_code, 201)

    def test_list_images(self):
        response = self.client.get('/api/images/list/')
        self.assertEqual(response.status_code, 200)

    def test_view_image(self):
        response = self.client.get(f'/api/images/{self.image_obj.id}/')
        self.assertEqual(response.status_code, 200)

    def test_delete_image(self):
        response = self.client.delete(f'/api/images/{self.image_obj.id}/delete/')
        self.assertEqual(response.status_code, 204)
