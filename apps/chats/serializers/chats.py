import logging

from rest_framework import serializers

from apps.chats.exceptions import (
    ChatTypeException,
    ChatWithoutEventException,
    DirectChatUserNotFoundException,
)
from apps.chats.models import Chat

logger = logging.getLogger("chats_app")


class ChatRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_chat_name")
    image_url = serializers.SerializerMethodField("get_chat_image_url")

    def get_chat_name(self, obj: Chat) -> str:
        chat_type_object = self.get_chat_type_object(obj)
        if obj.type == Chat.Type.EVENT:
            return chat_type_object.name
        elif obj.type == Chat.Type.DIRECT:
            return chat_type_object.username
        else:
            raise ChatTypeException("Chat type is not supported")

    def get_chat_image_url(self, obj: Chat) -> str:
        chat_type_object = self.get_chat_type_object(obj)
        return chat_type_object.image_url

    def get_chat_type_object(self, obj: Chat):
        if obj.type == Chat.Type.EVENT:
            try:
                event = obj.chat_event
            except Exception as exc:
                logger.error(f"Chat {obj} with the 'Event' type has no linked Event: " f"{exc}")
                raise ChatWithoutEventException

            return event

        elif obj.type == Chat.Type.DIRECT:
            direct_chat_user = obj.participants.exclude(
                id=self.context.get("request").user.id
            ).first()

            if not direct_chat_user:
                logger.error(f"Chat {obj} with the 'Direct' type has no the second user")
                raise DirectChatUserNotFoundException

            return direct_chat_user

        else:
            logger.error(f"{self.__class__.__name__}: Chat {obj} type error")
            raise ChatTypeException

    class Meta:
        model = Chat
        fields = ["id", "name", "image_url", "type"]


class ChatListSerializer(ChatRetrieveSerializer):
    last_message_text = serializers.CharField(max_length=528)
    last_message_is_owner = serializers.BooleanField()

    class Meta:
        model = Chat
        fields = ["id", "name", "image_url", "type", "last_message_text", "last_message_is_owner"]
