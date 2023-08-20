from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.events.models import Event
from apps.events.serializers import (
    EventListSerializer,
    EventRetrieveSerializer,
    EventCreateSerializer,
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
