from django.urls import path, include

from rest_framework import routers
from apps.profiles.viewsets import (
    ProfileViewSet,
    UserRatingViewSet,
    MyProfileViewSet,
    FollowerViewSet, ProfileEventViewSet,
)

app_name = "profiles"
router = routers.SimpleRouter()

router.register('users/(?P<user_id>[^/.]+)/user_ratings', UserRatingViewSet, basename="UserRating")
router.register("users", ProfileViewSet, basename="Profiles")
router.register("users", FollowerViewSet, basename="Followers")
router.register("users", ProfileEventViewSet, basename="User events")


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/me", MyProfileViewSet.as_view(), name="me"),
]
