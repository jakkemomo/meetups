from django.urls import include, path
from rest_framework import routers

from .viewsets import (
    ChatViewSet,
    ChatMessagesViewSet,
    ChatParticipantsViewSet,
    DirectChatViewSet,
    MessageViewSet,
)


app_name = "chats"

router = routers.SimpleRouter()
router.register("chats", ChatViewSet, basename="Chats")
router.register("chats", ChatMessagesViewSet, basename="ChatMessages")
router.register("chats", ChatParticipantsViewSet, basename="ChatParticipants")

router.register("messages", MessageViewSet, basename="Messages")
router.register("chats/users", DirectChatViewSet, basename="Directs")
urlpatterns = [path("api/v1/", include(router.urls))]
