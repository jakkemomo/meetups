import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView, \
    TokenObtainPairView

from apps.core import helpers
from apps.core.serializers import RegisterSerializer, \
    TokenVerifyResponseSerializer, TokenBlacklistResponseSerializer, \
    TokenRefreshResponseSerializer, TokenObtainPairResponseSerializer, \
    RegisterResponseSerializer, \
    ReverifyEmailSerializer, PasswordResetSerializer, \
    PasswordChangeSerializer
from apps.profiles.models import User

logger = logging.getLogger("core_app")


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: RegisterResponseSerializer,
        },
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=['auth'],
        manual_parameters=[openapi.Parameter('user_id', openapi.IN_QUERY,
                                             description="user unique id",
                                             type=openapi.TYPE_STRING),
                           openapi.Parameter('confirmation_token',
                                             openapi.IN_QUERY,
                                             description="confirmation token",
                                             type=openapi.TYPE_STRING)],
        responses={
            status.HTTP_200_OK: 'Email successfully confirmed',
            status.HTTP_400_BAD_REQUEST: 'Token is invalid or expired',
            status.HTTP_404_NOT_FOUND: 'User not found',
        },
    )
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.warning(f'warning: {__name__}: {exc}')
            user = None
        if user is None:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if user.is_email_verified:
            return Response('Email is already verified',
                            status=status.HTTP_400_BAD_REQUEST)
        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                'Token is invalid or expired. Please request another confirmation email by signing in.',
                status=status.HTTP_400_BAD_REQUEST)
        user.is_email_verified = True
        user.save()
        return Response('Email successfully confirmed')


class ReverifyEmailView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReverifyEmailSerializer

    @swagger_auto_schema(
        tags=['auth'],
        responses={
            status.HTTP_200_OK: 'Email successfully sent',
            status.HTTP_400_BAD_REQUEST: 'Email is already verified',
            status.HTTP_404_NOT_FOUND: 'User not found',
            status.HTTP_500_INTERNAL_SERVER_ERROR: 'Could not send message at the moment, try later',
        },
    )
    def post(self, request, *args, **kwargs):
        user = User.objects.get(email=request.data['email'])
        if not user:
            return Response('User not found', status=status.HTTP_404_NOT_FOUND)
        if user.is_email_verified:
            return Response('Email is already verified',
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            helpers.send_verification_email(user)
        except Exception as e:
            logging.error(e)
            return Response(
                'Could not send message at the moment, try later',
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response('Email successfully sent')


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenVerifyResponseSerializer,
        },
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenBlacklistView(TokenBlacklistView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenBlacklistResponseSerializer,
        },
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenRefreshResponseSerializer,
        },
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: TokenObtainPairResponseSerializer,
        },
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordResetView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"detail": "Email is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data.get("user")
        if not user:
            return Response(
                data={"detail": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            helpers.send_reset_password_email(user)

        except Exception as exc:
            logger.error(f'Error type: {type(exc).__name__}, '
                         f'location: {__name__}, user id: {user.id}')
            return Response(
                data={"detail": "An error occurred while sending an email. "
                                "Please try again later"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "Reset password email sent"},
            status=status.HTTP_201_CREATED,
        )


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=['auth'],
        manual_parameters=[
            openapi.Parameter(
                'user_id', openapi.IN_QUERY,
                description="user unique id",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'confirmation_token',
                openapi.IN_QUERY,
                description="confirmation token",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def get(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id', '')
        confirmation_token = request.query_params.get('confirmation_token', '')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.warning(f'warning: {__name__}: {exc}')
            user = None

        if not user:
            return Response(
                'User not found',
                status=status.HTTP_404_NOT_FOUND
            )

        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                data='Token is invalid or expired. '
                     'Please request another password changing.',
                status=status.HTTP_401_UNAUTHORIZED,
            )

        reset_token = default_token_generator.make_token(user)
        return Response({"reset_token": reset_token})


class PasswordChangeView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordChangeSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="user unique id",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'reset_token',
                openapi.IN_QUERY,
                description="reset token",
                type=openapi.TYPE_STRING,
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user_id = request.query_params.get('user_id', '')
        reset_token = request.query_params.get('reset_token', '')
        user_model = get_user_model()

        try:
            user = user_model.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.warning(f'warning: {__name__}: {exc}')
            user = None

        if not user:
            return Response(
                data='User not found',
                status=status.HTTP_404_NOT_FOUND,
            )

        if not default_token_generator.check_token(user, reset_token):
            return Response(
                data='Token is invalid or expired. '
                     'Please request another password changing.',
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not serializer.is_valid(raise_exception=True):
            return Response(
                {"detail": "Password is invalid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response('Your password has been changed')
