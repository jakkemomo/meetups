from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.core.files.storage import default_storage

import logging

from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from apps.upload.serializers import (
    UploadSerializer,
)
from .utils import upload_image


logger = logging.getLogger("upload_app")


class UploadViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, ]
    # renderer_classes = [JSONRenderer]
    serializer_class = UploadSerializer
    http_method_names = ["post", ]

    @swagger_auto_schema(operation_description='Upload file...')
    @action(detail=False, methods=["post", ])
    def create(self, request):
        file = request.data.get("file")
        serializer = self.serializer_class(data={"file": file})

        if serializer.is_valid(raise_exception=False):
            file = serializer.validated_data["file"]
            rel_url = upload_image(file)
            if rel_url:
                return Response(
                    status=201,
                    data={"url": default_storage.url(rel_url)},
                )
            else:
                return Response(
                    status=500,
                    data={"Error": "Internal server error"},
                )
        else:
            return Response(
                status=415,
                data={
                    "Error":
                        f"{file.content_type} extension is not supported. "
                        f"Supported extensions are: {serializer.allowed_extensions}"
                },
            )
