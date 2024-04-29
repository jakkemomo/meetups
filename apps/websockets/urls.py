from django.urls import re_path, path, include
from rest_framework import routers

from apps.websockets.consumers import NotificationConsumer, ChatConsumer
from apps.websockets.viewsets import ChatViewSet, MessageViewSet

app_name = "websockets"

router = routers.SimpleRouter()
router.register("chats", ChatViewSet, basename="Chats")
router.register("messages", MessageViewSet, basename="Messages")
urlpatterns = [
    path("api/v1/", include(router.urls)),
]

websocket_urlpatterns = [
    re_path(r"ws/notifications/", NotificationConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<chat_id>[^/.]+)", ChatConsumer.as_asgi()),
]
