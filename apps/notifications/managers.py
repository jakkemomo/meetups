from asgiref.sync import sync_to_async

from apps.notifications.base import BaseManager
from apps.notifications.models import Notification


class NotificationManager(BaseManager):
    @staticmethod
    async def notification(created_by, recipient, notification_type, additional_data):
        notification_object = await sync_to_async(Notification.objects.create)(
            created_by=created_by,
            recipient=recipient,
            type=notification_type,
            additional_data=additional_data,
        )
        recipient = notification_object.recipient
        created_by = notification_object.created_by
        created_at = notification_object.created_at
        data = {
            "notification_type": notification_type,
            "to_user_id": recipient.id,
            "to_username": recipient.username,
            "from_user_id": created_by.id,
            "from_username": created_by.username,
            "from_user_image_url": created_by.image_url,
            "follower_status": notification_object.additional_data.get("follower_status"),
        }

        await NotificationManager.send_data(
            type="notification",
            recipient=recipient.id,
            data=data,
            created_at=created_at,
        )
