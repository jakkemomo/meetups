from typing import Union

from asgiref.sync import async_to_sync
from django.forms import model_to_dict
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.chats.managers import ChatManager
from apps.chats.models import Chat, Message
from apps.chats.permissions.chats import ChatPermissions, DirectChatPermissions
from apps.chats.serializers.chats import ChatListSerializer, ChatRetrieveSerializer
from apps.chats.serializers.messages import MessageCreateSerializer, MessageRetrieveSerializer
from apps.chats.utils import list_chats_raw
from apps.events.filters import TrigramSimilaritySearchFilter
from apps.events.serializers import EmptySerializer
from apps.events.serializers.events import ParticipantSerializer
from apps.notifications.handlers.in_app import InAppNotificationsHandler
from apps.notifications.managers.chain import NotificationsChainManager
from apps.notifications.models import Notification
from apps.profiles.models import User
from apps.profiles.serializers import ProfileRetrieveSerializer


class ChatViewSet(viewsets.ModelViewSet):
    model = Chat
    permission_classes = [IsAuthenticated, ChatPermissions]
    lookup_url_kwarg = "chat_id"
    http_method_names = ["get", "post"]

    # Notifications
    handlers = (InAppNotificationsHandler(),)
    notifications_manager = NotificationsChainManager(handlers)

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

        self.queryset = self.model.objects.raw(
            list_chats_raw, [self.request.user.id, self.request.user.id, self.request.user.id]
        )
        return self.queryset

    # @swagger_auto_schema(request_body=no_body)
    # @action(methods=["get"], detail=True, url_path="messages", url_name="chat_messages")
    # def messages(self, request, chat_id):
    #     chat_object: Chat = self.get_object()
    #     messages = Message.objects.filter(chat_id=chat_object.id).order_by("-created_at")
    #     page = self.paginate_queryset(messages)
    #     serializer = self.get_serializer(page, many=True)
    #     return self.get_paginated_response(serializer.data)

    # @swagger_auto_schema(request_body=no_body)
    # @action(methods=["get"], detail=True, url_path="participants", url_name="chat_participants")
    # def participants(self, request, chat_id):
    #     chat_object: Chat = self.get_object()
    #     participants = User.objects.filter(
    #         id__in=chat_object.participants.all().values_list("id", flat=True)
    #     )
    #     page = self.paginate_queryset(participants)
    #     serializer = self.get_serializer(page, many=True)
    #     return self.get_paginated_response(serializer.data)

    @action(methods=["post"], detail=True, url_path="send_message", url_name="send_message")
    def send_message(self, request, chat_id):
        """
        CREATE method for messages but with sending it
        via notifications to the provided chats if exists
        """
        chat_object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Message creation and sending via ws
        message_object = async_to_sync(ChatManager.chat_message)(
            created_by=request.user,
            chat=chat_object,
            message_text=serializer.validated_data.get("message_text"),
        )

        # Notifications sending
        for participant in chat_object.participants.exclude(pk=request.user.id):
            self.notifications_manager.handle(
                created_by=request.user,
                recipient=participant,
                notification_type=Notification.Type.NEW_MESSAGE,
                additional_data={"message_text": message_object.message_text},
            )

        return Response(status=status.HTTP_201_CREATED, data=model_to_dict(message_object))

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass


class ChatMessagesViewSet(mixins.ListModelMixin, GenericViewSet):
    model = Message
    permission_classes = [IsAuthenticated, ChatPermissions]
    lookup_url_kwarg = "message_id"
    queryset = Message.objects.all()
    serializer_class = MessageRetrieveSerializer
    filter_backends = [TrigramSimilaritySearchFilter]
    search_fields = ["message_text", "created_by__username"]

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        if chat_id:
            chat = Chat.objects.get(id=chat_id)
            self.check_object_permissions(self.request, chat)
            self.queryset = (
                self.model.objects.filter(chat_id=chat_id)
                .select_related("created_by")
                .order_by("-created_at")
            )
        else:
            self.queryset = (
                self.model.objects.filter(
                    chat__in=Chat.objects.filter(participants__id=self.request.user.id)
                )
                .select_related("created_by")
                .order_by("-created_at")
            )

        return self.queryset

    @swagger_auto_schema(request_body=no_body)
    @action(
        methods=["get"],
        detail=False,
        url_path="(?P<chat_id>[^/.]+)/messages",
        url_name="chat_messages",
    )
    def chat_messages(self, request, chat_id):
        return self.list(request, chat_id=chat_id)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=["get"], detail=False, url_path="all/messages", url_name="all_chat_messages")
    def all_chat_messages(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ChatParticipantsViewSet(mixins.ListModelMixin, GenericViewSet):
    model = User
    permission_classes = [IsAuthenticated, ChatPermissions]
    lookup_url_kwarg = "user_id"
    queryset = User.objects.all()
    serializer_class = ProfileRetrieveSerializer
    filter_backends = [TrigramSimilaritySearchFilter]
    search_fields = ["username", "first_name", "last_name", "email"]

    def get_queryset(self):
        chat_id = self.kwargs.get("chat_id")
        if chat_id:
            chat = Chat.objects.get(id=chat_id)
            self.check_object_permissions(self.request, chat)
            self.queryset = self.model.objects.filter(
                id__in=chat.participants.all().values_list("id", flat=True)
            )
        else:
            raise ValidationError("Chat id is required")
        return self.queryset

    @swagger_auto_schema(request_body=no_body)
    @action(
        methods=["get"],
        detail=False,
        url_path="(?P<chat_id>[^/.]+)/participants",
        url_name="chat_participants",
    )
    def chat_participants(self, request, chat_id):
        return self.list(request, chat_id=chat_id)


class DirectChatViewSet(viewsets.ModelViewSet):
    model = User
    permission_classes = [IsAuthenticated, DirectChatPermissions]
    lookup_url_kwarg = "user_id"
    http_method_names = ["post"]
    queryset = User.objects.all()
    serializer_class = ChatRetrieveSerializer

    @swagger_auto_schema(request_body=no_body)
    @action(
        methods=["post"], detail=True, url_path="direct", url_name="get_or_create_user_direct_chat"
    )
    def get_or_create_user_direct_chat(self, request, user_id):
        user: User = self.get_object()
        if user == request.user:
            return Response(
                status=status.HTTP_400_BAD_REQUEST, data="You can't chat with yourself"
            )

        try:
            chat_object: Union[Chat, None] = (
                Chat.objects.filter(participants=user, type=Chat.Type.DIRECT)
                .filter(participants=request.user)
                .first()
            )
        except Chat.DoesNotExist:
            chat_object = None

        code = status.HTTP_200_OK

        if not chat_object:
            chat_object: Chat = Chat.objects.create(type=Chat.Type.DIRECT)
            chat_object.participants.add(user, request.user)
            chat_object.save()
            code = status.HTTP_201_CREATED

        serializer = self.get_serializer(chat_object)
        return Response(status=code, data=serializer.data)

    @swagger_auto_schema(auto_schema=None)
    def create(self, request, *args, **kwargs):
        pass
