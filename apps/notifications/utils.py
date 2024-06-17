import json

from django.template.loader import render_to_string
from django.contrib.auth.models import User

from apps.core.helpers import send_email
from apps.notifications.models import Notification


def send_notification_email(
        created_by: User,
        recipient: User,
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
