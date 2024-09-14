from rest_framework import serializers

from apps.chats.models import Message
from apps.chats.serializers.base import SendingBaseSerializer


class MessageRetrieveSerializer(SendingBaseSerializer):
    username = serializers.CharField(source="created_by.username", read_only=True)

    class Meta:
        model = Message
        fields = [
            "id",
            "created_by",
            "username",
            "chat",
            "message_text",
            "created_at",
            "image_url",
            "status",
            "read_at",
        ]


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["id", "message_text"]


class MessageDeleteSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False, write_only=True
    )


class MessageMarkReadSerializer(serializers.Serializer):
    ids = serializers.ListField(
        child=serializers.IntegerField(), allow_empty=False, write_only=True
    )
