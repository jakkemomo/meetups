from rest_framework import serializers

from apps.chats.models import Message


class MessageRetrieveSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj: Message) -> str:
        return obj.created_by.image_url

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
