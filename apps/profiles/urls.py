from django.urls import path, include

from rest_framework import routers
from apps.profiles.viewsets import ProfileViewSet, UserRatingViewSet

app_name = "profiles"
router = routers.SimpleRouter()

router.register('user/(?P<user_id>[^/.]+)/user_ratings', UserRatingViewSet, basename="UserRating")
router.register("profiles", ProfileViewSet, basename="Profiles")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
