from django.urls import path, include
from rest_framework import routers

from .views import EventCreation, EventDetail, EventEdition, EventListing, EventMap, EventDeletion
from .views import RegisterToEvent, LeaveFromEvent, RateEvent
from .viewsets import EventViewSet

app_name = "events"

router = routers.SimpleRouter()
router.register("events", EventViewSet, basename="Events")


urlpatterns = [
    path("events/map/", EventMap.as_view(), name="event_map"),
    # path("events/list/", EventListing.as_view(), name="event_list"),
    path("events/create/", EventCreation.as_view(), name="event_creation"),
    # path("events/<str:pk>/", EventDetail.as_view(), name="event_detail"),
    path("events/<str:pk>/update/", EventEdition.as_view(), name="event_edition"),
    path("events/<str:pk>/delete/", EventDeletion.as_view(), name="event_deletion"),
    # path("events/<int:event_id>/register/", RegisterToEvent.as_view(), name="Events-event_register"),
    # path("events/<int:event_id>/leave/", LeaveFromEvent.as_view(), name="leave_from_event"),
    # path("events/<int:event_id>/rate/<int:value>", RateEvent.as_view(), name="rate_an_event"),
    # path("events/<int:event_id>/remove_rating/", RateEvent.as_view(), name="remove_rating"),
    path("events/<int:event_id>/register/", RegisterToEvent.as_view(), name="register_to_event"),
    path("events/<int:event_id>/leave/", LeaveFromEvent.as_view(), name="leave_from_event"),
    path(
        "events/<str:pk>/create_rating/",
        RateEvent.as_view(),
        name="rating_creation",
    ),
    path(
        "events/<str:pk>/update_rating/",
        RateEvent.as_view(),
        name="rating_edition",
    ),
    path(
        "events/<str:pk>/delete_rating/",
        RateEvent.as_view(),
        name="rating_deletion",
    ),
    # rest
    path("api/v1/", include(router.urls)),
]
