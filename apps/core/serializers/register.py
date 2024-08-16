from django.contrib.auth.password_validation import validate_password
from django.utils.module_loading import import_string
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.core import helpers
from apps.profiles.models import User
from config import settings


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, min_length=2, max_length=128)
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"].lower()
        )
        user.set_password(validated_data["password"])
        user.image_url = settings.DEFAULT_USER_AVATAR_URL
        user.save()

        # Notification preferences creating
        preferences = [import_string(i) for i in settings.NOTIFICATION_PREFERENCES.values()]
        for preference_model in preferences:
            preference_model.objects.create(user=user)

        try:
            helpers.send_verification_email(
                user,
                url=settings.VERIFY_EMAIL_URL,
                email=validated_data["email"].lower()
            )
        except Exception as e:
            user.delete()
            raise e

        return user


class RegisterResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
