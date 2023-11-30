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
        }
    )
    email = EmailMessage(subject, message, to=[user.email])
    email.content_subtype = 'html'

    email.send()
