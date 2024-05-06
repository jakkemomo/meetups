from django.urls import path, include
from rest_framework import routers

from .viewsets import (
    EventViewSet,
    RatingViewSet,
    TagViewSet,
    MarkerViewSet,
    CategoryViewSet,
    ReviewViewSet,
    CurrencyViewSet,
    ParticipantViewSet
)


app_name = "events"

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="Events")
router.register("events/(?P<event_id>[^/.]+)/ratings", RatingViewSet, basename="Events rating")
router.register("categories", CategoryViewSet, basename="Categories")
router.register("tags", TagViewSet, basename="Tags")
router.register("markers", MarkerViewSet, basename="Markers")
router.register("currencies", CurrencyViewSet, basename="Currencies")
router.register("events/(?P<event_id>[^/.]+)/review", ReviewViewSet, basename="Review")
router.register("events", ParticipantViewSet, basename="Events participants")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
