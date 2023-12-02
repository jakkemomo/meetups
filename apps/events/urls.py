from django.urls import path, include
from rest_framework import routers

from .viewsets import EventViewSet, RatingViewSet, TagViewSet, MarkerViewSet

app_name = "events"

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="Events")
router.register("events/(?P<event_id>[^/.]+)/ratings", RatingViewSet, basename="Events rating")
router.register("tags", TagViewSet, basename="Tags")
router.register("markers", MarkerViewSet, basename="Markers")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
