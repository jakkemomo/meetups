import logging

from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.upload.serializers import UploadSerializer

from .utils import upload_image

logger = logging.getLogger("upload_app")


class UploadViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser]
    serializer_class = UploadSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(operation_description="Upload file...")
    @action(detail=False, methods=["post"])
    def create(self, request):
        file = request.data.get("file")
        serializer = self.serializer_class(data={"file": file})

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY, data=e.detail)

        file = serializer.validated_data["file"]
        rel_url = upload_image(file)

        if not rel_url:
            return Response(status=500, data={"Error": "Internal server error"})

        return Response(
            status=201, data={"url": rel_url, "test_url": default_storage.url(rel_url)}
        )
