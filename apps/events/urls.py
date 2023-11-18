from django.urls import path, include
from rest_framework import routers

from .views import EventCreation, EventEdition, EventMap, EventDeletion
from .viewsets import EventViewSet, RatingViewSet, TagViewSet, MarkerViewSet

app_name = "events"

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="Events")
router.register("events/(?P<event_id>[^/.]+)/ratings", RatingViewSet, basename="Events rating")

router.register("tags", TagViewSet, basename="Tags")
router.register("markers", MarkerViewSet, basename="Markers")

urlpatterns = [
    path("events/map/", EventMap.as_view(), name="event_map"),
    # path("events/list/", EventListing.as_view(), name="event_list"),
    path("events/create/", EventCreation.as_view(), name="event_creation"),
    # path("events/<str:pk>/", EventDetail.as_view(), name="event_detail"),
    path("events/<str:pk>/update/", EventEdition.as_view(), name="event_edition"),
    path("events/<str:pk>/delete/", EventDeletion.as_view(), name="event_deletion"),
    # path("events/<int:event_id>/register/", RegisterToEvent.as_view(), name="Events-event_register"),
    # path("events/<int:event_id>/leave/", LeaveFromEvent.as_view(), name="leave_from_event"),
    # rest
    path("api/v1/", include(router.urls)),
]
