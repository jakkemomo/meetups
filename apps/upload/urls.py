from django.template.defaulttags import url
from django.urls import path, include
from .viewsets import UploadViewSet
from rest_framework.routers import SimpleRouter

app_name = "upload"

# router = SimpleRouter()
# router.register("image", UploadViewSet, basename="upload_image")

urlpatterns = [
    path("api/v1/upload", UploadViewSet.as_view()),
]
