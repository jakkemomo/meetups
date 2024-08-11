from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter

from apps.events.filters import TrigramSimilaritySearchFilter
from apps.events.models import Event
from apps.events.permissions import EventPermissions
from apps.events.serializers.events import ParticipantSerializer
from apps.profiles.models import User


class ParticipantViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    model = User
    serializer_class = ParticipantSerializer
    lookup_url_kwarg = "user_id"
    filter_backends = [TrigramSimilaritySearchFilter, OrderingFilter, DjangoFilterBackend]
    search_fields = ["username", "email"]
    ordering_fields = ["username", "email"]
    permission_classes = [EventPermissions]

    def get_queryset(self, *args, **kwargs):
        if self.kwargs.get("event_id"):
            self.queryset = (
                Event.objects.filter(id=self.kwargs["event_id"]).first().participants.all()
            )
            return self.queryset
        else:
            raise Http404("Event not found")

    @action(
        methods=["get"],
        detail=False,
        url_path="(?P<event_id>[^/.]+)/participants",
        url_name="event_list_participants",
    )
    def list_user_is_participant(self, request, event_id):
        self.check_object_permissions(request, Event.objects.get(id=event_id))
        return super().list(request)
