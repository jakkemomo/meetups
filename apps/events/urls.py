from django.urls import path, include
from rest_framework import routers

from .viewsets.events import EventViewSet
from .viewsets.ratings import RatingViewSet
from .viewsets.tags import TagViewSet
from .viewsets.markers import MarkerViewSet
from .viewsets.categories import CategoryViewSet
from .viewsets.reviews import ReviewViewSet
from .viewsets.currencies import CurrencyViewSet
from .viewsets.participants import ParticipantViewSet

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
