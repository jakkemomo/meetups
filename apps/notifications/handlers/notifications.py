from apps.notifications.handlers.base import AbstractHandler
from apps.notifications.managers.in_app import InAppNotificationManager


class InAppNotificationsHandler(AbstractHandler):
    async def handle(
            self, created_by, recipient,
            notification_type, additional_data
    ):
        if recipient.in_app_notifications_allowed:
            await InAppNotificationManager.notification(
                created_by=created_by,
                recipient=recipient,
                notification_type=notification_type,
                additional_data=additional_data
            )
