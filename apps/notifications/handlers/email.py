from django.utils.module_loading import import_string
from django.contrib.auth.models import User

from apps.notifications.handlers.base import AbstractNotificationsHandler
from apps.notifications.models import Notification
from apps.notifications.utils import send_notification_email
from config import settings


class EmailNotificationsHandler(AbstractNotificationsHandler):
    def notify(
            self,
            created_by: User,
            recipient: User,
            notification_type: Notification.Type,
            additional_data: dict
    ):
        send_notification_email(
            created_by=created_by,
            recipient=recipient,
            notification_type=notification_type,
            additional_data=additional_data
        )

    def get_preferences_model(self):
        return import_string(settings.PREFERENCES.get("EMAIL"))
