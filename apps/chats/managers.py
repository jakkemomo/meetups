from asgiref.sync import sync_to_async

from apps.chats.models import Message
from apps.notifications.base import BaseManager


class ChatManager(BaseManager):
    @staticmethod
    async def chat_message(created_by, chat, message_text):
        message_object = await sync_to_async(Message.objects.create)(
            created_by=created_by,
            chat=chat,
            message_text=message_text
        )

        data = {
            "to_chat_id": message_object.chat.id,
            "from_user_id": message_object.created_by.id,
            "message_text": message_object.message_text,
        }
        await ChatManager.send_data(
            type="chat_message",
            recipient=message_object.chat.id,
            data=data,
            created_at=message_object.created_at
        )

        return message_object
