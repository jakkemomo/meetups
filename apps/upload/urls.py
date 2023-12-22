from django.urls import path

from .viewsets import UploadViewSet

app_name = "upload"

urlpatterns = [
    path("api/v1/upload", UploadViewSet.as_view()),
]
