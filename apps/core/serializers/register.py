from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.core import helpers
from apps.profiles.models import User
from config import settings


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, min_length=2, max_length=128,
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"].lower(),
        )
        user.set_password(validated_data["password"])
        user.image_url = settings.DEFAULT_USER_AVATAR_URL
        user.save()

        try:
            helpers.send_verification_email(user, url=settings.VERIFY_EMAIL_URL)
        except Exception as e:
            user.delete()
            raise e

        return user


class RegisterResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
