from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.core.serializers.tokens import (
    TokenBlacklistResponseSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenVerifyResponseSerializer}, tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenBlacklistResponseSerializer}, tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenRefreshResponseSerializer}, tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer}, tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        if request.user.is_email_verified:
            return super().post(request, *args, **kwargs)
        else:
            return Response(
                data={"user.is_email_verified": "False, but must be True"},
                status=status.HTTP_403_FORBIDDEN,
            )
