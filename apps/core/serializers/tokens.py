from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from config import settings


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
        attrs[self.username_field] = attrs[self.username_field].lower()
        return super().validate(attrs)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["aud"] = "WEB"
        token["iss"] = settings.SERVICE_URL

        return token
