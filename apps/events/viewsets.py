from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.events.models import Event
from apps.events.serializers import (
    EventListSerializer,
    EventRetrieveSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    model = Event
    # queryset = Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        match self.action:
            case "retrieve":
                self.queryset = Event.objects.filter(id=self.kwargs["pk"])
            case _:
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

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="register",
        url_name="event_register",
    )
    def register_for_event(self, request, pk: int):
        event = get_object_or_404(Event, id=pk)
        event.participants.add(request.user.id)
        event.current_participants_number += 1
        event.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="leave",
        url_name="event_leave",
    )
    def leave_from_event(self, request, pk=None):
        event = get_object_or_404(Event, id=pk)
        event.participants.remove(request.user.id)
        event.current_participants_number -= 1
        event.save()
        return Response(status=status.HTTP_200_OK)
