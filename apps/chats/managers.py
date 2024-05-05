from apps.chats.models import Message
from apps.notifications.base import BaseManager


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
