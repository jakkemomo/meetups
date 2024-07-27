from django.urls import path, include

from rest_framework import routers
from .viewsets import (
    ProfileViewSet,
    MyProfileViewSet,
    FollowerViewSet,
    UserRatingViewSet,
    ProfileEventViewSet,
)
from ..notifications.viewsets.preferences import (
    InAppNotificationsPreferencesViewSet,
    EmailNotificationsPreferencesViewSet,
)

app_name = "profiles"
router = routers.SimpleRouter()

router.register('users/(?P<user_id>[^/.]+)/ratings', UserRatingViewSet, basename="UserRating")
router.register("users", ProfileViewSet, basename="Profiles")
router.register("users", FollowerViewSet, basename="Followers")
router.register("users", ProfileEventViewSet, basename="User events")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/me", MyProfileViewSet.as_view(), name="me"),
    path(
        "api/v1/me/preferences/notifications/email",
        EmailNotificationsPreferencesViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update"}
        ),
        name="Email Notifications Preferences"
    ),
    path(
        "api/v1/me/preferences/notifications/in_app",
        InAppNotificationsPreferencesViewSet.as_view(
            {"get": "retrieve", "put": "update", "patch": "partial_update"}
        ),
        name="In-App Notifications Preferences"
    ),
]
