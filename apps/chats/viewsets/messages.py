from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.chats.models import Chat, Message
from apps.chats.permissions.message import MessagePermissions
from apps.chats.serializers.messages import MessageCreateSerializer, MessageRetrieveSerializer
from apps.events.serializers import EmptySerializer


class MessageViewSet(viewsets.ModelViewSet):
    model = Message
    permission_classes = [IsAuthenticated, MessagePermissions]
    lookup_url_kwarg = "message_id"
    http_method_names = ["get", "patch", "delete"]
    queryset = model.objects.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return MessageRetrieveSerializer
            case "list":
                return MessageRetrieveSerializer
            case "partial_update":
                return MessageCreateSerializer
            case _:
                return EmptySerializer

    def get_queryset(self):
        if self.kwargs.get("message_id"):
            self.queryset = self.model.objects.all()
        else:
            self.queryset = self.model.objects.filter(
                id__in=Chat.objects.filter(participants__id=self.request.user.id).values_list(
                    "chat_messages", flat=True
                )
            ).order_by("-created_at")
        return self.queryset.all()
