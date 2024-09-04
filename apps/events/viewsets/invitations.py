from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.events.models.invitations import Invitation
from apps.events.permissions import EventPermissions
from apps.events.serializers import InvitationSerializer


class InvitationViewSet(viewsets.ModelViewSet):
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()
    model = Invitation
    permission_classes = [IsAuthenticatedOrReadOnly, EventPermissions]
    lookup_url_kwarg = "event_id"
    http_method_names = ["post", "get", "delete"]
