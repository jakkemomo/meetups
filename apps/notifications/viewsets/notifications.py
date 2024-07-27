from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.serializers import EmptySerializer
from apps.notifications.models import Notification
from apps.notifications.permissions.notifications import (
    NotificationsPermissions,
)
from apps.notifications.serializers.notifications import (
    NotificationsRetrieveSerializer
)


class NotificationsViewSet(viewsets.GenericViewSet,
                           viewsets.mixins.ListModelMixin,
                           viewsets.mixins.RetrieveModelMixin):
    model = Notification
    permission_classes = [IsAuthenticated, NotificationsPermissions]
    lookup_url_kwarg = "notification_id"

    def get_queryset(self):
        queryset = (
            self.model.objects
            .filter(recipient=self.request.user, status=Notification.Status.NEW)
            .order_by("-created_at")
        )
        return queryset.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return NotificationsRetrieveSerializer
            case "list":
                return NotificationsRetrieveSerializer
            case _:
                return EmptySerializer

    @swagger_auto_schema(
        method="patch",
        manual_parameters=[
            openapi.Parameter(
                'notification_ids',
                openapi.IN_QUERY,
                description="List of notification IDs to be marked as read, separated by commas",
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                required=True
            )
        ],
        request_body=no_body,
        responses={200: "Notifications marked as read."}
    )
    @action(
        methods=["patch"],
        detail=False,
        url_path="read",
        permission_classes=[IsAuthenticated],
        url_name="mark_as_read",
    )
    def mark_notifications_as_read(self, request):
        notification_ids = request.query_params.get("notification_ids", '')
        if not notification_ids:
            return Response({"detail": "No notification IDs provided."},
                            status=status.HTTP_400_BAD_REQUEST)
        ids = list(map(int, notification_ids.split(",")))
        notifications = self.model.objects.filter(id__in=ids,
                                                  recipient=request.user)
        updated_count = notifications.update(status=Notification.Status.READ)

        return Response({"detail": f"{updated_count} notifications marked as read."},
                        status=status.HTTP_200_OK)
