from django.urls import path, include

from rest_framework import routers
from apps.profiles.viewsets.ratings import UserRatingViewSet
from apps.profiles.viewsets.profiles import (
    ProfileViewSet,
    MyProfileViewSet,
)
from apps.profiles.viewsets.followers import FollowerViewSet
from apps.events.viewsets.events import ProfileEventViewSet

app_name = "profiles"
router = routers.SimpleRouter()

router.register('users/(?P<user_id>[^/.]+)/ratings', UserRatingViewSet, basename="UserRating")
router.register("users", ProfileViewSet, basename="Profiles")
router.register("users", FollowerViewSet, basename="Followers")
router.register("users", ProfileEventViewSet, basename="User events")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/me", MyProfileViewSet.as_view(), name="me"),
]
