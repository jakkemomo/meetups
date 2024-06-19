from django.urls import path, include
from rest_framework import routers

from .viewsets import NotificationsViewSet

app_name = "notifications"

router = routers.SimpleRouter()
router.register("notifications", NotificationsViewSet, basename="Notifications")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
