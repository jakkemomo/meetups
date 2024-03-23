from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class NotificationManager:
    @staticmethod
    def send_notification(sender, recipient, event, notification_type):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(recipient),
            {
                "type": notification_type,
                "event": event,
                "from_user": sender,
            }
        )

    @staticmethod
    def follow(user_id, follower_id):
        event = f"User {follower_id} followed user {user_id}"
        NotificationManager.send_notification(
            sender=follower_id,
            recipient=user_id,
            event=event,
            notification_type="follow",
        )

    @staticmethod
    def follow_request(user_id, follower_id):
        event = f"User {follower_id} sent follow request to user {user_id}"
        NotificationManager.send_notification(
            sender=follower_id,
            recipient=user_id,
            event=event,
            notification_type="follow_request",
        )

    @staticmethod
    def accept_follow_request(user_id, follower_id):
        event = f"User {user_id} accepted follow request of user {follower_id}"
        NotificationManager.send_notification(
            sender=user_id,
            recipient=follower_id,
            event=event,
            notification_type="accept_follow_request",
        )
