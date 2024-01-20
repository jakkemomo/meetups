import json

from django.core.files.storage import default_storage
from django.core.serializers import serialize
from django.db.models import Q, Count
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.events.models import Event, Rating, Tag
from apps.events.permissions import RatingPermissions, EventPermissions, TagPermissions
from apps.events.serializers import (
    EventListSerializer,
    EventRetrieveSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
    RatingCreateSerializer,
    RatingRetrieveSerializer,
    RatingUpdateSerializer,
    RatingListSerializer,
    TagCreateSerializer,
    TagRetrieveSerializer,
    TagUpdateSerializer,
    TagListSerializer,
    GeoJsonSerializer,
    EventRegisterSerializer
)

from apps.core.utils import delete_image_if_exists
import logging

logger = logging.getLogger("events_app")


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    def destroy(self, request, *args, **kwargs):
        event_instance = self.get_object()
        delete_image_if_exists(event_instance)
        # Proceed with the standard destroy operation
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        event_instance = self.get_object()
        if event_instance.image_url != request.data.get(
                'image_url') :
            delete_image_if_exists(event_instance)

        # Proceed with the standard update operation
        return super().update(request, *args, **kwargs)

    model = Event
    permission_classes = [IsAuthenticatedOrReadOnly, EventPermissions]
    lookup_url_kwarg = "event_id"

    def get_template_names(self):
        match self.action:
            case "retrieve":
                return ["events/detail.html"]
            case "list":
                return ["events/list.html"]
            case "create":
                return ["events/creation.html"]
            case "update":
                return ["events/edition.html"]
            case "partial_update":
                return ["events/edition.html"]
            case "destroy":
                return ["events/event_confirm_delete.html"]
            case "register_for_event":
                return ["events/detail.html"]
            case "leave_from_event":
                return ["events/detail.html"]

    def get_queryset(self):
        if self.kwargs.get("pk"):
            self.queryset = Event.objects.filter(id=self.kwargs["pk"])
        else:
            if self.request.user.id:
                self.queryset = self.model.objects.filter(
                    Q(is_visible=True) & Q(is_finished=False)
                    | Q(participants__in=[self.request.user.id]) & Q(is_finished=False)
                ).distinct()
            else:
                self.queryset = self.model.objects.filter(
                    Q(is_visible=True) & Q(is_finished=False)
                )
        return self.queryset.all().annotate(participants_number=Count("participants"))

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return EventRetrieveSerializer
            case "list":
                return EventListSerializer
            case "create":
                return EventCreateSerializer
            case "update":
                return EventUpdateSerializer
            case "partial_update":
                return EventUpdateSerializer
            case "register_for_event":
                return EventRegisterSerializer
            case "leave_from_event":
                return EventRegisterSerializer

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[EventPermissions],
        url_path="register",
        url_name="event_register",
    )
    def register_for_event(self, request, event_id: int):
        event = self.get_object()
        event.participants.add(request.user.id)
        event.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[EventPermissions],
        url_path="leave",
        url_name="event_leave",
    )
    def leave_from_event(self, request, event_id: int):
        event = self.get_object()
        event.participants.remove(request.user.id)
        event.save()
        return Response(status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event ratings.
    """

    model = Rating
    permission_classes = [IsAuthenticatedOrReadOnly, RatingPermissions]
    lookup_url_kwarg = "rating_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        event = self.get_object()
        self.queryset = Rating.objects.filter(event=event, user=self.request.user)
        return self.queryset.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return RatingRetrieveSerializer
            case "create":
                return RatingCreateSerializer
            case "update":
                return RatingUpdateSerializer
            case "list":
                return RatingListSerializer

    def list(self, request, *args, **kwargs):
        event = self.get_object()
        queryset = Rating.objects.filter(event=event)
        serializer = RatingListSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event Tags.
    """

    model = Tag
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, TagPermissions]
    lookup_url_kwarg = "tag_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return TagRetrieveSerializer
            case "create":
                return TagCreateSerializer
            case "update":
                return TagUpdateSerializer
            case "list":
                return TagListSerializer


class MarkerViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
    serializer_class = GeoJsonSerializer

    @swagger_auto_schema(
        tags=['map'],
        operation_description="Get all events in GeoJSON format",
    )
    def list(self, request, *args, **kwargs):
        geo_events = json.loads(
            serialize(
                "geojson", self.queryset.all(),
                geometry_field="location",
                fields=["id", "name", "start_date", "end_date", "description", "address"])
        )
        return Response(geo_events, status=status.HTTP_200_OK)
