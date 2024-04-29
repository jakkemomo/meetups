from rest_framework import permissions

from apps.websockets.models import Chat


class ChatPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Chat):
        return request.user in obj.participants.all()
