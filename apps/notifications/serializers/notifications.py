from apps.chats.serializers.base import SendingBaseSerializer
from apps.notifications.models import Notification


class NotificationsRetrieveSerializer(SendingBaseSerializer):
    class Meta:
        model = Notification
        fields = [
            "id",
            "created_by",
            "recipient",
            "created_at",
            "type",
            "additional_data",
            "image_url",
        ]
