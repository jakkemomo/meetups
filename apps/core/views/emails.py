import logging
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.core import helpers
from apps.core.helpers import decode_json_data
from apps.core.serializers.emails import EmailCheckSerializer, ReverifyEmailSerializer
from apps.profiles.models import User
from config import settings

logger = logging.getLogger("core_app")


class VerifyEmailView(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=["auth"],
        manual_parameters=[
            openapi.Parameter(
                "token", openapi.IN_QUERY, description="token", type=openapi.TYPE_STRING
            )
        ],
        responses={
            status.HTTP_200_OK: '{"refresh": ..., "access": ...}',
            status.HTTP_400_BAD_REQUEST: "Token is invalid or expired OR "
            "Email is already verified",
            status.HTTP_404_NOT_FOUND: "User not found",
        },
    )
    def get(self, request, *args, **kwargs):
        token = request.query_params.get("token")

        try:
            data = decode_json_data(token)
        except Exception as exc:
            logger.error(f"Decoding failed: {exc}")

            return Response("Invalid payload.", status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = data["user_id"]
            confirmation_token = data["confirmation_token"]
        except KeyError as exc:
            logger.warning(f"Data not found: {exc}")

            return Response("Invalid token.", status=status.HTTP_400_BAD_REQUEST)

        user_model = get_user_model()

        try:
            user = user_model.objects.get(id=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.error(exc)

            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        if user.is_email_verified:
            return Response("Email is already verified", status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, confirmation_token):
            return Response(
                "Token is invalid or expired. "
                "Please request another confirmation email by signing in.",
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.is_email_verified = True
        user.save()

        refresh = RefreshToken.for_user(user)
        refresh.access_token.set_exp(lifetime=timedelta(hours=1))

        return Response(data={"access": str(refresh.access_token)}, status=status.HTTP_200_OK)


class ReverifyEmailView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ReverifyEmailSerializer

    @swagger_auto_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: "Email successfully sent",
            status.HTTP_400_BAD_REQUEST: "Email is already verified",
            status.HTTP_404_NOT_FOUND: "User not found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Could not send message at the moment, try later",
        },
    )
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data["email"].lower()).first()
        if not user:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        if user.is_email_verified:
            return Response("Email is already verified", status=status.HTTP_400_BAD_REQUEST)
        try:
            helpers.send_verification_email(user, url=settings.VERIFY_EMAIL_URL)
        except Exception as e:
            logging.error(e)
            return Response(
                "Could not send message at the moment, try later",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response("Email successfully sent")


class ChangeEmailView(APIView):
    """
    This view handles email change requests from authenticated users.
    Validates the user's email, send message to email for verification email.
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ReverifyEmailSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(
        tags=["auth"],
        responses={
            status.HTTP_200_OK: "Email successfully sent",
            status.HTTP_409_CONFLICT: "Email exist",
            status.HTTP_404_NOT_FOUND: "User not found",
            status.HTTP_500_INTERNAL_SERVER_ERROR: "Could not send message at the moment, try later",
        },
    )
    def post(self, request, *args, **kwargs):
        user_model = get_user_model()
        try:
            user = user_model.objects.get(id=request.user.id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as exc:
            logger.error(exc)

            return Response("User not found", status=status.HTTP_404_NOT_FOUND)
        if not request.data.get("email"):
            return Response(status=status.HTTP_400_BAD_REQUEST, data="Email is required")
        email = request.data["email"].lower()
        if User.objects.filter(email=email).exists():
            return Response(
                status=status.HTTP_409_CONFLICT, data="This email has already been registered"
            )
        # user.is_email_verified = False
        # user.email = email
        # user.save()
        try:
            helpers.send_verification_email(user, url=settings.CHANGE_EMAIL_URL)
        except Exception as e:
            logging.error(e)
            return Response(
                "Could not send message at the moment, try later",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(status=status.HTTP_200_OK, data="Email successfully sent")


class CheckEmailExistsView(APIView):
    """
    This view checks if a user with a certain email exists in the database.
    """

    queryset = User.objects.all()
    permission_classes = (AllowAny,)  # Allow any user (authenticated or not) to access this view
    serializer_class = EmailCheckSerializer

    def get_serializer(self, *args, **kwargs):
        """
        This function is using to generate swagger documents.
        """
        return self.serializer_class(self, *args, **kwargs)

    @swagger_auto_schema(tags=["auth"])
    def post(self, request, *args, **kwargs):
        """
        Checks the database for a user with the given email address.
        Input: email
        Result: A boolean indicating whether a user with the email exists
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email", "")  # Email is taken from serializer
        user_exists = User.objects.filter(email=email.lower()).exists()
        return Response(user_exists)
