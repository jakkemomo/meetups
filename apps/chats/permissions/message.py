from rest_framework import permissions

from apps.chats.models import Message
from apps.core.permissions import is_owner


class MessagePermissions(permissions.BasePermission):
    """
    Is owner or readonly if participant of a message chats
    """
    def has_object_permission(self, request, view, obj: Message):
        if request.user not in obj.chat.participants.all():
            return False
        elif request.method in permissions.SAFE_METHODS:
            return True

        return is_owner(request, obj)
