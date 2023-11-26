from io import BytesIO
import re

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from PIL import Image

from apps.upload.utils import task_logger


class UploadSerializer(serializers.Serializer):
    allowed_extensions = ['png', 'jpg', 'jpeg', 'svg', 'webp']
    file = serializers.ImageField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=allowed_extensions,
            ),
        ],
    )

    def validate_file(self, file):
        if file.content_type != "image/webp":
            return self.convert_to_webp(file)
        return file

    @staticmethod
    @task_logger
    def convert_to_webp(raw_file):
        with Image.open(raw_file) as image:
            file = BytesIO()
            image.save(file, format="webp")

        file.seek(0)
        file = SimpleUploadedFile(
            name=raw_file.name,
            content=file.getvalue(),
            content_type="image/webp",
        )
        file.name = re.sub(r'\.\w+$', '.webp', file.name)
        return file
