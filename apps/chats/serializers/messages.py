from rest_framework import serializers

from apps.chats.models import Message
from apps.chats.serializers.base import SendingBaseSerializer


class MessageRetrieveSerializer(SendingBaseSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "created_by",
            "chat",
            "message_text",
            "created_at",
            "image_url",
        ]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = [
            "id",
            "message_text",
        ]
