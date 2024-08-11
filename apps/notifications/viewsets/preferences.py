from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.notifications.exceptions import MissingPreferencesObjectException
from apps.notifications.models import EmailNotificationsPreferences, InAppNotificationsPreferences
from apps.notifications.permissions.preferences import NotificationsPreferencesPermissions
from apps.notifications.serializers.preferences import (
    EmailNotificationsPreferencesRetrieveSerializer,
    EmailNotificationsPreferencesUpdateSerializer,
    InAppNotificationsPreferencesRetrieveSerializer,
    InAppNotificationsPreferencesUpdateSerializer,
)


class BaseNotificationsPreferencesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, NotificationsPreferencesPermissions]
    http_method_names = ["get", "put", "patch"]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        queryset = self.model.objects.filter(user=self.request.user)
        return queryset.all()

    def get_object(self):
        queryset = self.get_queryset()
        preferences_object = queryset.first()
        if not preferences_object:
            raise MissingPreferencesObjectException

        self.check_object_permissions(self.request, preferences_object)

        return preferences_object


class EmailNotificationsPreferencesViewSet(BaseNotificationsPreferencesViewSet):
    model = EmailNotificationsPreferences

    def get_serializer_class(self):
        match self.action:
            case "update":
                return EmailNotificationsPreferencesUpdateSerializer
            case "partial_update":
                return EmailNotificationsPreferencesUpdateSerializer
            case _:
                return EmailNotificationsPreferencesRetrieveSerializer


class InAppNotificationsPreferencesViewSet(BaseNotificationsPreferencesViewSet):
    model = InAppNotificationsPreferences

    def get_serializer_class(self):
        match self.action:
            case "update":
                return InAppNotificationsPreferencesUpdateSerializer
            case "partial_update":
                return InAppNotificationsPreferencesUpdateSerializer
            case _:
                return InAppNotificationsPreferencesRetrieveSerializer
