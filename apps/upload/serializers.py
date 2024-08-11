import uuid
from io import BytesIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.validators import FileExtensionValidator
from PIL import Image
from rest_framework import serializers

from apps.upload.utils import task_logger


class UploadSerializer(serializers.Serializer):
    allowed_extensions = ["png", "jpg", "jpeg", "svg", "webp"]
    file = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=allowed_extensions)]
    )

    def validate_file(self, file):
        self.validate_resolution(file)
        if file.content_type != "image/webp":
            file = self.convert_to_webp(file)
        file.name = f"{uuid.uuid4().hex}.webp"
        return file

    @staticmethod
    @task_logger
    def convert_to_webp(raw_file):
        with Image.open(raw_file) as image:
            file = BytesIO()
            image.save(file, format="webp")

        file.seek(0)
        file = SimpleUploadedFile(
            name=raw_file.name, content=file.getvalue(), content_type="image/webp"
        )
        return file

    @staticmethod
    def validate_resolution(file):
        with Image.open(file) as image:
            width, height = image.size
            if width < 800 or height < 600:
                raise ValidationError("The image resolution should be at least 800x600 pixels")
