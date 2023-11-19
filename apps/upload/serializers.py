from django.core.validators import FileExtensionValidator
from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.ImageField()

    def validate(self, data):
        validators = [
            FileExtensionValidator(
                allowed_extensions=['png', 'jpeg', 'jpg', 'svg']),
        ]
        for validator in validators:
            validator(data.file.name)

    class Meta:
        fields = [
            "file",
        ]
