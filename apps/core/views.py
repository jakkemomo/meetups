from django.contrib.auth import login as auth_login
from django.contrib.auth.views import LoginView, LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.core.forms import CustomUserCreationForm


class CoreSignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("events:event_map")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        result = super(CoreSignUpView, self).form_valid(form)
        auth_login(self.request, self.object)
        return result


class CoreLoginView(LoginView):
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")


class CoreLogoutView(DjangoLogoutView):
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenRefreshResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenVerifyResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TokenBlacklistResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: TokenBlacklistResponseSerializer})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
