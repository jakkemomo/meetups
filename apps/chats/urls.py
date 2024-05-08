from django.urls import path, include
from rest_framework import routers

from apps.chats.viewsets import (
    ChatViewSet,
    MessageViewSet,
    DirectChatViewSet,
)

app_name = "chats"

router = routers.SimpleRouter()
router.register("chats", ChatViewSet, basename="Chats")
router.register("messages", MessageViewSet, basename="Messages")
router.register("chats/users", DirectChatViewSet, basename="Directs")
urlpatterns = [
    path("api/v1/", include(router.urls)),
]
