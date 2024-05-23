from asgiref.sync import sync_to_async

from apps.notifications.handlers.base import AbstractHandler
from apps.notifications.utils import send_notification_email


class EmailNotificationsHandler(AbstractHandler):
    async def handle(
            self, created_by, recipient,
            notification_type, additional_data
    ):
        if recipient.email_notifications_allowed:
            await sync_to_async(send_notification_email)(
                recipient=recipient,
                created_by=created_by,
                notification_type=notification_type,
                additional_data=additional_data
            )
