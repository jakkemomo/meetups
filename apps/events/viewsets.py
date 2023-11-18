from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from apps.events.models import Event, Rating, Tag
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
)


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    model = Event
    # queryset = Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
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
        return self.queryset.all()

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

    @swagger_auto_schema(auto_schema=None)
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="register",
        url_name="event_register",
    )
    def register_for_event(self, request, event_id: int):
        # resp = services.Events(register, event_id, request.user.id)
        # return resp
        event = get_object_or_404(Event, id=event_id)
        event.participants.add(request.user.id)
        event.current_participants_number += 1
        event.save()
        return Response(data=EventRetrieveSerializer(event).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="leave",
        url_name="event_leave",
    )
    def leave_from_event(self, request, event_id: int):
        event = get_object_or_404(Event, id=event_id)
        event.participants.remove(request.user.id)
        event.current_participants_number -= 1
        event.save()
        return Response(data=EventRetrieveSerializer(event).data, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event ratings.
    """

    model = Rating
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
    lookup_url_kwarg = "rating_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        event = get_object_or_404(Event, id=self.kwargs.get("event_id"))
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
        event = get_object_or_404(Event, id=kwargs.get("event_id"))
        queryset = Rating.objects.filter(event=event)
        serializer = RatingListSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data)


class TagViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event Tags.
    """

    model = Tag
    permission_classes = [IsAuthenticatedOrReadOnly]
    renderer_classes = [TemplateHTMLRenderer, JSONRenderer]
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
