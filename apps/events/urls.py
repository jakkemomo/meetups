from django.urls import path, include
from rest_framework import routers

from .views import EventCreation, EventDetail, EventEdition, EventListing, EventMap, EventDeletion
from .views import RegisterToEvent, LeaveFromEvent, RateEvent
from .viewset import EventViewSet

app_name = "events"

router = routers.SimpleRouter()
router.register("events", EventViewSet)


urlpatterns = [
    path("map/", EventMap.as_view(), name="event_map"),
    path("list/", EventListing.as_view(), name="event_list"),
    path("create/", EventCreation.as_view(), name="event_creation"),
    path("<str:pk>/", EventDetail.as_view(), name="event_detail"),
    path("<str:pk>/update/", EventEdition.as_view(), name="event_edition"),
    path("<str:pk>/delete/", EventDeletion.as_view(), name="event_deletion"),
    path("events/<int:event_id>/register/", RegisterToEvent.as_view(), name="register_to_event"),
    path("events/<int:event_id>/leave/", LeaveFromEvent.as_view(), name="leave_from_event"),
    path("events/<int:event_id>/rate/<int:value>", RateEvent.as_view(), name="rate_an_event"),
    path("events/<int:event_id>/remove_rating/", RateEvent.as_view(), name="remove_rating"),
    path("api/v1/", include(router.urls)),
]
