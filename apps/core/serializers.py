from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core import helpers
from apps.profiles.models import User


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, min_length=4, max_length=15, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

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

    def validate(self, attrs):
        username = attrs["username"]
        user_model = get_user_model()
        try:
            user = user_model.objects.get(Q(username=username) | Q(email=username.lower()))
            attrs['username'] = user.username
        except user_model.DoesNotExist:
            return None
        data = super(TokenPairSerializer, self).validate(attrs)
        return data


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
                {"email": "There are no users with that Email address!"}
            )

        if not user.is_email_verified:
            raise serializers.ValidationError(
                {"email": "Email is not verified!"}
            )

        return attrs


class PasswordFormSerializer(serializers.Serializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    confirmed_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match"}
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
        if not user:
            raise serializers.ValidationError(
                {"user": "The user is not authenticated"}
            )

        if user.check_password(attrs["password"]):
            raise serializers.ValidationError(
                {"password": "The new password is the same as old one"}
            )
        if not user.check_password(attrs["old_password"]):
            raise serializers.ValidationError(
                {"old_password": "Existing password is incorrect"}
            )

        return attrs
