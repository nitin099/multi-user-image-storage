from django.db import models

class Image(models.Model):
    file_name = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=255)
    metadata = models.JSONField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id}"
