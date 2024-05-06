from rest_framework import permissions

from apps.notifications.models import Notification


class NotificationsPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Notification):
        return is_recipient(request, obj)


def is_recipient(request, obj):
    return request.user == obj.recipient
