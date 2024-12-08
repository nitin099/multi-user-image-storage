# multi-user-image-storage
This is a Django-based image storage service designed to handle multiple users concurrently. It integrates:

LocalStack S3 for storing images
MongoDB for persisting image metadata
Django REST Framework for building APIs
The service allows users to upload, view, download, list, and delete images with associated metadata.

# Features
Multi-user support: Each user can manage their own images and metadata.
S3 Integration: Images are stored in LocalStack's S3 simulation.
NoSQL Metadata: Metadata is stored in MongoDB for flexibility and scalability.
RESTful APIs: Easily integrate with frontend or other services.
Swagger Documentation: Interactive API documentation for testing and exploration.

# Create an S3 bucket in LocalStack:

```bash
Copy code
aws --endpoint-url=http://localhost:4566 s3 mb s3://localstack-bucket

## Installation

Follow these steps to set up the project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/multi-user-image-storage.git
cd multi-user-image-storage

### 2. Set Up Virtual Environment
Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
```

# Configuration

Django Settings
Update settings.py for S3 and MongoDB:

MongoDB: Ensure MongoDB is running locally on port 27017.
S3: Use LocalStack endpoint:


```
AWS_ACCESS_KEY_ID = "test"
AWS_SECRET_ACCESS_KEY = "test"
AWS_STORAGE_BUCKET_NAME = "localstack-bucket"
AWS_S3_ENDPOINT_URL = "http://localhost:4566"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'image_metadata_db',
    }
}
```