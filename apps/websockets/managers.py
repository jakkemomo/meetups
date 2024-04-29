from apps.websockets.base import BaseManager
from apps.websockets.models import Notification, Message


class NotificationManager(BaseManager):
    @staticmethod
    def follow(notification_object: Notification):
        recipient = notification_object.recipient
        created_by = notification_object.created_by
        created_at = notification_object.created_at
        data = {
            "to_user_id": recipient.id,
            "to_username": recipient.username,
            "from_user_id": created_by.id,
            "from_username": created_by.username,
            "from_user_image_url": created_by.image_url,
            "follower_status": notification_object.additional_data.get("follower_status"),
        }
        NotificationManager.send_data(
            type="follow_notification",
            recipient=recipient.id,
            data=data,
            created_at=created_at,
        )

    @staticmethod
    def follow_request(notification_object):
        recipient = notification_object.recipient
        created_by = notification_object.created_by
        created_at = notification_object.created_at
        data = {
            "to_user_id": recipient.id,
            "to_username": recipient.username,
            "from_user_id": created_by.id,
            "from_username": created_by.username,
            "from_user_image_url": created_by.image_url,
            "follower_status": notification_object.additional_data.get("follower_status"),
        }
        NotificationManager.send_data(
            type="follow_request_notification",
            recipient=recipient.id,
            data=data,
            created_at=created_at,
        )

    @staticmethod
    def accept_follow_request(notification_object):
        recipient = notification_object.recipient
        created_by = notification_object.created_by
        created_at = notification_object.created_at
        data = {
            "to_user_id": recipient.id,
            "to_username": recipient.username,
            "from_user_id": created_by.id,
            "from_username": created_by.username,
            "from_user_image_url": created_by.image_url,
            "follower_status": notification_object.additional_data.get("follower_status"),
        }
        NotificationManager.send_data(
            type="accept_follow_request_notification",
            recipient=recipient.id,
            data=data,
            created_at=created_at,
        )


class ChatManager(BaseManager):
    @staticmethod
    def chat_message(message_object: Message):
        created_by = message_object.created_by
        chat = message_object.chat
        message_text = message_object.message_text
        created_at = message_object.created_at
        data = {
            "to_chat_id": chat.id,
            "from_user_id": created_by.id,
            "message_text": message_text,
        }
        ChatManager.send_data(
            type="chat_message",
            recipient=chat.id,
            data=data,
            created_at=created_at
        )
