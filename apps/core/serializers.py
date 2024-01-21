from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

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
        user.save()

        try:
            helpers.send_verification_email(user)
        except Exception as e:
            user.delete()
            raise e

        return user


class RegisterResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class ReverifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("email",)


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['aud'] = 'WEB'
        token['iss'] = settings.SERVICE_URL

        return token


class PasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = ("email", )

    def validate(self, attrs):
        email = attrs["email"]
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
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, attrs):
        super().validate(attrs)

        user = self.context.get("user")
        if not user:
            raise serializers.ValidationError(
                {"user": "The user is not authenticated"}
            )

        if user.check_password(attrs["password"]):
            raise serializers.ValidationError(
                {"password": "The new password is the same as old one"}
            )

        return attrs


class PasswordChangeSerializer(PasswordFormSerializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, attrs):
        super().validate(attrs)

        user = self.context.get("user")
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Existing password is incorrect"}
            )

        return attrs


class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False
        self.user = None

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
        }

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        data = {}

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
