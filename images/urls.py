from django.urls import path
from .views import UploadImageView, ListImagesView, ViewImageView, DeleteImageView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('list/', ListImagesView.as_view(), name='list-images'),
    path('view/<int:image_id>/', ViewImageView.as_view(), name='view-image'),
    path('<int:pk>/delete/', DeleteImageView.as_view(), name='delete-image'),
]