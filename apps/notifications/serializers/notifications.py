from rest_framework import serializers

from apps.chats.serializers.base import SendingBaseSerializer
from apps.notifications.models import Notification


class NotificationsRetrieveSerializer(SendingBaseSerializer):
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True,
    )
    recipient_username = serializers.CharField(
        source='recipient.username',
        read_only=True,
    )

    class Meta:
        model = Notification
        fields = [
            "id",
            "created_by",
            "created_by_username",
            "recipient",
            "recipient_username",
            "created_at",
            "type",
            "text",
            "additional_data",
            "image_url",
        ]
