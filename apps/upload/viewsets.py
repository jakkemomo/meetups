from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from apps.upload.serializers import (
    UploadSerializer,
)
from .utils import upload_image


class UploadViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, ]
    # renderer_classes = [JSONRenderer]
    serializer_class = UploadSerializer
    http_method_names = ["post", ]

    @swagger_auto_schema(operation_description='Upload file...')
    @action(detail=False, methods=["post", ])
    def post(self, request):
        file = request.FILES.get('file')
        serializer = self.serializer_class(data={"file": file})

        if serializer.is_valid():
            url = upload_image(file)
            return Response(status=201, data={"url": url})
        else:
            return Response(
                status=400,
                data={"Error": f"{file.content_type} files are not supported"}
            )
