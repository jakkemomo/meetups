from datetime import datetime

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationManager:
    @staticmethod
    def send_notification(sender, recipient, data, notification_type):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(recipient),
            {
                "type": notification_type,
                "from_user": sender,
                "to_user": recipient,
                "data": data,
                "created": datetime.now().isoformat()
            }
        )

    @staticmethod
    def follow(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "user_id": user.id,
            "user_username": user.username,
            "follower_id": follower.id,
            "follower_username": follower.username,
            "follower_image_url": follower.image_url,
            "following_status": follower_object.status,
        }
        NotificationManager.send_notification(
            sender=follower.id,
            recipient=user.id,
            data=data,
            notification_type="follow",
        )

    @staticmethod
    def follow_request(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "user_id": user.id,
            "user_username": user.username,
            "follower_id": follower.id,
            "follower_username": follower.username,
            "follower_image_url": follower.image_url,
            "following_status": follower_object.status,
        }
        NotificationManager.send_notification(
            sender=follower.id,
            recipient=user.id,
            data=data,
            notification_type="follow_request",
        )

    @staticmethod
    def accept_follow_request(follower_object):
        user = follower_object.user
        follower = follower_object.follower
        data = {
            "user_id": user.id,
            "user_username": user.username,
            "user_image_url": user.image_url,
            "follower_id": follower.id,
            "follower_username": follower.username,
            "following_status": follower_object.status,
        }
        NotificationManager.send_notification(
            sender=user.id,
            recipient=follower.id,
            data=data,
            notification_type="accept_follow_request",
        )
