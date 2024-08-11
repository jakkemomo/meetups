from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from django.utils.module_loading import import_string

from apps.notifications.handlers.base import AbstractNotificationsHandler
from apps.notifications.managers.in_app import InAppNotificationManager
from apps.notifications.models import Notification
from config import settings


class InAppNotificationsHandler(AbstractNotificationsHandler):
    def notify(
        self,
        created_by: User,
        recipient: User,
        notification_type: Notification.Type,
        additional_data: dict,
    ):
        async_to_sync(InAppNotificationManager.notification)(
            created_by=created_by,
            recipient=recipient,
            notification_type=notification_type,
            additional_data=additional_data,
        )

    def get_preferences_model(self):
        return import_string(settings.NOTIFICATION_PREFERENCES.get("IN_APP"))
