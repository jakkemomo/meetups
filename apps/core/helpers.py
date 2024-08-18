import base64
import json
from typing import Any

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config import settings


def send_email(user: User, subject, message):
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = "html"

    email.send()


def send_verification_email(user, url: str, email):
    confirmation_token = default_token_generator.make_token(user)
    data = {"user_id": user.id, "confirmation_token": confirmation_token, "email": email}

    token = encode_json_data(data)

    verification_link = f"{url}" f"?token={token}"

    subject = "Activate your account"
    message = render_to_string(
        "emails/email_verification.html",
        {"link": verification_link, "base_url": settings.SERVICE_URL},
    )

    send_email(user=user, subject=subject, message=message)


def send_reset_password_email(user):
    reset_token = default_token_generator.make_token(user)
    data = {"user_id": user.id, "reset_token": reset_token}

    token = encode_json_data(data)

    verification_link = f"{settings.CONFIRM_PASSWORD_RESET_URL}" f"?token={token}"
    subject = "Confirm password reset"
    message = render_to_string(
        "emails/reset_password.html", {"verification_link": verification_link}
    )

    send_email(user=user, subject=subject, message=message)


def encode_json_data(data: dict) -> str:
    """
    This function creates url-safe encoded token to secure a dict with data
    """
    handled_data = json.dumps(data).encode("utf-8")
    token = base64.urlsafe_b64encode(handled_data).decode("utf-8")

    return token


def decode_json_data(token: str) -> Any:
    """
    This function decodes url-safe token to a dict with data
    """
    data = json.loads(base64.urlsafe_b64decode(token).decode("utf-8"))

    return data
