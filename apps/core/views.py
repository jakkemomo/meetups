import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenBlacklistView, TokenVerifyView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView,
)
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core import helpers
from apps.core.serializers import (
    RegisterSerializer,
    TokenVerifyResponseSerializer,
    TokenBlacklistResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenObtainPairResponseSerializer,
    RegisterResponseSerializer,
    ReverifyEmailSerializer,
    PasswordResetSerializer,
    PasswordChangeSerializer,
    PasswordFormSerializer,
    EmailCheckSerializer,
)
from apps.profiles.models import User
from apps.core.helpers import decode_json_data

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
            status.HTTP_200_OK: '{"refresh": ..., "access": ...}',
            status.HTTP_400_BAD_REQUEST: "Token is invalid or expired OR "
                                         "Email is already verified",
            status.HTTP_404_NOT_FOUND: "User not found",
        }

    )
    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')

        try:
            data = decode_json_data(token)
        except Exception as exc:
            logger.warning(f'Decoding failed: {exc}')

            return Response(
                'Invalid payload.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user_id = data['user_id']
            confirmation_token = data['confirmation_token']
        except KeyError as exc:
            logger.warning(f'Data not found: {exc}')

            return Response(
                'Invalid token.',
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_model = get_user_model()

        try:
            user = user_model.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.warning(f'warning: {__name__}: {exc}')

            return Response(
                'User not found',
                status=status.HTTP_404_NOT_FOUND
            )

        if user.is_email_verified:
            return Response(
                'Email is already verified',
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                'Token is invalid or expired. '
                'Please request another confirmation email by signing in.',
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_email_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(hours=1))

        return Response(
            data={
                'access': str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


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
        user = User.objects.filter(email=request.data['email']).first()
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
    """
    This view handles password reset requests from unauthenticated users.
    Validates the user's email, generates a 'reset_token', and sends an email
    with a password reset link containing the 'token'.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordResetSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        """
        Validates the user's email from the request data,
        generates a reset token, and sends a reset password email to the user.
        The email contains a link with  encrypted JSON data
        (including 'user_id' and 'reset_token') as a
        'token' in the query parameters.

        Input: User's email
        Result: Email with 'reset_token' sent
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
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
    """
    This view handles password reset confirmations.
    Decodes the 'user_id' and 'reset_token' from the provided 'token' in the
    URL, validates them, and changes the user's password to the new one
    provided in the request data.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PasswordFormSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
        manual_parameters=[
            openapi.Parameter(
                'token',
                openapi.IN_QUERY,
                description="token",
                type=openapi.TYPE_STRING
            )
        ],
    )
    def post(self, request, *args, **kwargs):
        """
        Decodes the JSON data from the 'token' in the query parameters of
        the request. Validates 'user_id', 'reset_token', and a new 'password'
        from the request data. If validation is successful,
        changes the user's password to the new one.

        Input: password
        Result: Password is changed
        """
        token = request.query_params.get('token', '')

        try:
            data = decode_json_data(token)
        except Exception as exc:
            logger.warning(f'Decoding failed: {exc}')
            data = None

        if not data:
            return Response(
                data={
                    "token": "Error decoding token. "
                             "Please ensure your token is valid and properly formatted."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_id = data.get('user_id', '')
        reset_token = data.get('reset_token', '')

        user_model = get_user_model()

        try:
            user = user_model.objects.get(id=user_id)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.warning(f'Post user failed: {exc}')
            user = None

        if not user:
            return Response(
                data={"user": "User not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not default_token_generator.check_token(user, reset_token):
            return Response(
                data={
                    "token": "Token is invalid or expired. "
                             "Please request another password changing.",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(
            data=request.data,
            context={"user": user}
        )

        if not serializer.is_valid():
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response(
            data={"detail": "Your password has been changed"},
            status=status.HTTP_200_OK,
        )


class PasswordChangeView(APIView):
    """
    This view handles the request of an authorised user
    who wants to change its password.
    It validates the old and new passwords from the request data
    and changes the user's password.
    """
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        """
        Validates the old and new passwords from the request data,
        then changes user's password.

        Input: old_password, password, confirmed_password
        Result: Password changed
        """
        user = request.user
        serializer = self.get_serializer(
            data=request.data,
            context={"user": user}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data["password"])
        user.save()

        return Response('Your password has been changed')


class CheckEmailExistsView(APIView):
    """
    This view checks if a user with a certain email exists in the database.
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Allow any user (authenticated or not) to access this view
    serializer_class = EmailCheckSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=['auth'],
    )
    def post(self, request, *args, **kwargs):
        """
        Checks the database for a user with the given email address.
        Input: email
        Result: A boolean indicating whether a user with the email exists
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email', '')  # Email is taken from serializer
        user_exists = User.objects.filter(email=email).exists()
        return Response(user_exists)
