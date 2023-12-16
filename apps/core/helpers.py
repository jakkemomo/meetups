from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config import settings


def send_verification_email(user):
    confirmation_token = default_token_generator.make_token(user)
    verification_link = f'{settings.VERIFY_EMAIL_URL}?user_id={user.id}&confirmation_token={confirmation_token}'
    subject = 'Activate your account'
    message = render_to_string(
        'emails/email_verification.html',
        {
            'link': verification_link,
            'base_url': settings.SERVICE_URL,
        }
    )
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'

    email.send()


def send_reset_password_email(user):
    confirmation_token = default_token_generator.make_token(user)
    verification_link = (
        f'{settings.CONFIRM_PASSWORD_RESET_URL}'
        f'?user_id={user.id}'
        f'&confirmation_token={confirmation_token}'
    )
    subject = 'Confirm password reset'
    message = (
        f'Please click on the following link to reset your password: '
        f'{verification_link}'
    )
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'

    email.send()
