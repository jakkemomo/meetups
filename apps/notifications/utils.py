import json

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from apps.core.helpers import send_email

user_model = get_user_model()


def send_notification_email(
        recipient, created_by,
        notification_type, additional_data
):
    subject = 'New notification'
    message = render_to_string(
        'emails/email_notification.html',
        {
            "from_username": created_by.username,
            "notification_type": notification_type,
            "additional_data": json.dumps(additional_data)
        }
    )

    send_email(user=recipient, subject=subject, message=message)