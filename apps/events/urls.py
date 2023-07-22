from django.urls import path

from .views import EventCreation, EventDetail, EventEdition, EventListing, EventMap, EventDeletion
from .views import RegisterToEvent, LeaveFromEvent

app_name = "events"

urlpatterns = [
    path("map/", EventMap.as_view(), name="event_map"),
    path("list/", EventListing.as_view(), name="event_list"),
    path("create/", EventCreation.as_view(), name="event_creation"),
    path("<str:pk>/", EventDetail.as_view(), name="event_detail"),
    path("<str:pk>/update/", EventEdition.as_view(), name="event_creation"),
    path("<str:pk>/delete/", EventDeletion.as_view(), name="event_deletion"),
    path("events/<int:event_id>/register/", RegisterToEvent.as_view(), name="register_to_event"),
    path("events/<int:event_id>/remove/", LeaveFromEvent.as_view(), name="leave_from_event"),
]
