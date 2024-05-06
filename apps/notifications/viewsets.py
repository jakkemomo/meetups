from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.events.serializers import EmptySerializer
from apps.notifications.models import Notification
from apps.notifications.permissions.notifications import (
    NotificationsPermissions,
)
from apps.notifications.serializers.notifications import (
    NotificationsRetrieveSerializer,
)


class NotificationsViewSet(viewsets.ModelViewSet):
    model = Notification
    permission_classes = [IsAuthenticated, NotificationsPermissions]
    lookup_url_kwarg = "notification_id"
    http_method_names = ["get"]

    def get_queryset(self):
        # TODO: is that a good approach to leave user only his notifications?
        # in that case, if user appeals to another user's notifications
        # he would have a 404 response
        # i think this is not bery RESTful but more safe 'cause he can't
        # recognise are there any other notifications besides his
        self.queryset = (
            self.model.objects
            .filter(recipient=self.request.user)
            .order_by("-created_at")
        )
        return self.queryset.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return NotificationsRetrieveSerializer
            case "list":
                return NotificationsRetrieveSerializer
            case _:
                return EmptySerializer
