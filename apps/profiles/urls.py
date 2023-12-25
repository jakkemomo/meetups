from django.urls import path, include
from rest_framework import routers
from apps.profiles.viewsets import ProfileViewSet

app_name = "profiles"

router = routers.SimpleRouter()
router.register("profiles", ProfileViewSet, basename="Profiles")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
