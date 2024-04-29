from rest_framework import permissions

from apps.core.permissions import is_owner
from apps.websockets.models import Message


class MessagePermissions(permissions.BasePermission):
    """
    Is owner or readonly if participant of a message chat
    """
    def has_object_permission(self, request, view, obj: Message):
        pass
        if (
                request.method in permissions.SAFE_METHODS
                and request.user in obj.chat.participants.all()
        ):
            return True

        return is_owner(request, obj)
