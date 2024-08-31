from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.chats.models import Chat, Message
from apps.chats.permissions.message import MessagePermissions
from apps.chats.serializers.messages import (
    MessageCreateSerializer,
    MessageRetrieveSerializer,
    MessageDeleteSerializer,
    MessageMarkReadSerializer,
)
from apps.events.serializers import EmptySerializer


class MessageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing message instances.
    """

    model = Message
    permission_classes = [IsAuthenticated, MessagePermissions]
    lookup_url_kwarg = "message_id"
    http_method_names = ["get", "patch", "delete"]
    queryset = model.objects.all()

    def get_serializer_class(self):
        if self.action in ["retrieve", "list"]:
            return MessageRetrieveSerializer
        elif self.action == "partial_update":
            return MessageCreateSerializer
        elif self.action == "mark_as_read":
            return MessageMarkReadSerializer
        return EmptySerializer

    def get_queryset(self):
        """
        Returns the queryset of messages. If a message_id is provided,
         all messages are returned.
        Otherwise, returns messages for chats the user participates in.
        """
        if self.kwargs.get("message_id"):
            self.queryset = self.model.objects.all()
        else:
            self.queryset = self.model.objects.filter(
                id__in=Chat.objects.filter(participants__id=self.request.user.id).values_list(
                    "chat_messages", flat=True
                )
            ).order_by("-created_at")
        return self.queryset.all()

    @swagger_auto_schema(
        method="delete",
        request_body=MessageDeleteSerializer,
        responses={
            200: openapi.Response(
                description="Successful deletion",
                examples={"application/json": {"message": "Deleted 3 items."}},
            ),
            400: openapi.Response(
                description="Bad Request: Invalid input",
                examples={"application/json": {"message": "Invalid input."}},
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {"message": "You can't delete other users' messages."}
                },
            ),
        },
    )
    @action(
        methods=["delete"], detail=False, permission_classes=[IsAuthenticated, MessagePermissions]
    )
    def delete(self, request: Request):
        """
        Deletes a list of messages specified by their IDs.

        Only the messages created by the requesting user can be deleted.
        """
        serializer = MessageDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        delete_ids = serializer.validated_data["ids"]

        delete_messages = self.get_queryset().filter(id__in=delete_ids)

        for message in delete_messages:
            if message.created_by != request.user:
                return Response(
                    {"message": "You can't delete other users' messages."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        delete_count = delete_messages.delete()

        return Response(
            {"message": f"Deleted {delete_count[0]} items."}, status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        method="patch",
        request_body=MessageMarkReadSerializer,
        responses={
            200: openapi.Response(
                description="Messages marked as read",
                examples={"application/json": {"message": "Marked 3 items as read."}},
            ),
            400: openapi.Response(
                description="Bad Request: Invalid input",
                examples={"application/json": {"message": "Invalid input."}},
            ),
            403: openapi.Response(
                description="Forbidden",
                examples={
                    "application/json": {"message": "You can't mark your own messages as read."}
                },
            ),
        },
    )
    @action(
        methods=["patch"], detail=False, permission_classes=[IsAuthenticated, MessagePermissions]
    )
    def mark_as_read(self, request: Request):
        """
        Marks a list of messages as read specified by their IDs.
        """
        serializer = MessageMarkReadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_ids = serializer.validated_data["ids"]

        messages_to_mark = self.get_queryset().filter(id__in=message_ids)

        for message in messages_to_mark:
            if message.created_by == request.user:
                return Response(
                    {"message": "You can't mark your own messages as read."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        updated_count = messages_to_mark.update(status=Message.Status.READ, read_at=timezone.now())

        return Response(
            {"message": f"Marked {updated_count} items as read."}, status=status.HTTP_200_OK
        )
