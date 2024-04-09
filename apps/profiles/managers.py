from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationManager:
    @staticmethod
    def send_notification(recipient, data, notification_type):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(recipient),
            {
                "type": notification_type,
                "data": data,
                "created": datetime.now().isoformat()
            }
        )

    @staticmethod
    def follow(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "to_user_id": user.id,
            "to_username": user.username,
            "from_user_id": follower.id,
            "from_username": follower.username,
            "from_user_image_url": follower.image_url,
            "follower_status": follower_object.status,
        }
        NotificationManager.send_notification(
            recipient=user.id,
            data=data,
            notification_type="follow",
        )

    @staticmethod
    def follow_request(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "to_user_id": user.id,
            "to_username": user.username,
            "from_user_id": follower.id,
            "from_username": follower.username,
            "from_user_image_url": follower.image_url,
            "follower_status": follower_object.status,
        }
        NotificationManager.send_notification(
            recipient=user.id,
            data=data,
            notification_type="follow_request",
        )

    @staticmethod
    def accept_follow_request(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "to_user_id": follower.id,
            "to_username": follower.username,
            "from_user_id": user.id,
            "from_username": user.username,
            "from_user_image_url": user.image_url,
            "follower_status": follower_object.status,
        }
        NotificationManager.send_notification(
            recipient=follower.id,
            data=data,
            notification_type="accept_follow_request",
        )
