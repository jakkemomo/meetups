import json

from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from apps.core.helpers import send_email
from apps.notifications.models import Notification

user_model = get_user_model()


def send_notification_email(
        created_by: user_model,
        recipient: user_model,
        notification_type: Notification.Type,
        additional_data: dict
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
