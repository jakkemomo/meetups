from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from apps.profiles.models import User


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email",)

    def validate(self, attrs):
        email = attrs["email"].lower()
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=email)
            attrs["user"] = user
        except user_model.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "There are no users with that Email address"}
            )

        return attrs


class PasswordFormSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    def validate(self, attrs):
        super().validate(attrs)

        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError({"user": "The user is not authenticated"})

        if user.check_password(attrs["password"]):
            raise serializers.ValidationError(
                {"password": "The new password is the same as old one"}
            )

        return attrs


class PasswordChangeSerializer(PasswordFormSerializer):
    old_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    def validate(self, attrs):
        super().validate(attrs)

        user = self.context.get("user")
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError({"old_password": "Existing password is incorrect"})

        return attrs
