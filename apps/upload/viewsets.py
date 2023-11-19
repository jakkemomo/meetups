from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from apps.upload.serializers import (
    UploadSerializer,
)
from .utils import upload_image
from rest_framework.mixins import CreateModelMixin


class UploadViewSet(CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, ]
    # renderer_classes = [JSONRenderer]
    serializer_class = UploadSerializer
    http_method_names = ["post", ]

    @swagger_auto_schema(operation_description='Upload file...', )
    @action(detail=False, methods=["post", ])
    def post(self, request):
        file = request.FILES.get('file')
        url = upload_image(file)
        return Response(status=201, data={"url": url})
