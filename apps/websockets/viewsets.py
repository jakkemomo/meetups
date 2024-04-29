import logging

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.forms import model_to_dict
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.serializers import EmptySerializer
from apps.events.serializers.events import ParticipantSerializer
from apps.websockets.managers import ChatManager
from apps.websockets.models import Chat, Message
from apps.websockets.permissions.chat import ChatPermissions
from apps.websockets.permissions.message import MessagePermissions
from apps.websockets.serializers.chat import (
    ChatRetrieveSerializer,
    ChatListSerializer,
)
from apps.websockets.serializers.message import (
    MessageRetrieveSerializer,
    MessageCreateSerializer,
)
from apps.websockets.utils import list_chats_raw

logger = logging.getLogger("websockets_app")

user_model = get_user_model()


class ChatViewSet(viewsets.ModelViewSet):
    model = Chat
    permission_classes = [IsAuthenticated, ChatPermissions]
    lookup_url_kwarg = "chat_id"
    http_method_names = ["list", "get", "post"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return ChatRetrieveSerializer
            case "list":
                return ChatListSerializer
            case "messages":
                return MessageRetrieveSerializer
            case "participants":
                return ParticipantSerializer
            case "send_message":
                return MessageCreateSerializer
            case _:
                return EmptySerializer

    def get_queryset(self):
        if self.kwargs.get("chat_id"):
            self.queryset = self.model.objects.all()
            return self.queryset.all()

        # TODO: it was easier to write a raw query, but it requires an approve
        self.queryset = self.model.objects.raw(
            list_chats_raw,
            [self.request.user.id, self.request.user.id]
        )
        return self.queryset

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=['get'],
        detail=True,
        url_path='messages',
        url_name='chat_messages'
    )
    def messages(self, request, chat_id):
        chat_object: Chat = self.get_object()
        messages = Message.objects.filter(chat_id=chat_object.id)
        page = self.paginate_queryset(messages)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=['get'],
        detail=True,
        url_path='participants',
        url_name='chat_participants'
    )
    def participants(self, request, chat_id):
        chat_object: Chat = self.get_object()
        participants = user_model.objects.filter(
            id__in=chat_object.participants.all().values_list("id", flat=True)
        )
        page = self.paginate_queryset(participants)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        url_path='send_message',
        url_name='send_message',
    )
    def send_message(self, request, chat_id):
        """
        CREATE method for messages but with sending it
        via websockets to the provided chat if exists
        """
        chat_object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_object = Message.objects.create(
            created_by=request.user,
            chat=chat_object,
            message_text=serializer.validated_data.get("message_text")
        )

        ChatManager.chat_message(message_object)

        return Response(
            status=status.HTTP_201_CREATED,
            data=model_to_dict(message_object),
        )

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass


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
                Q(created_by=self.request.user) |
                Q(id__in=Chat.objects.filter(
                    participants__id=self.request.user.id
                ).values_list("chat_messages", flat=True))
            )
        return self.queryset.all()
