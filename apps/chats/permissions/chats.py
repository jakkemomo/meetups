from rest_framework import permissions

from apps.chats.models import Chat
from apps.profiles.utils import is_follower



class ChatPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Chat):
        return request.user in obj.participants.all()


class DirectChatPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action == "get_or_create_user_direct_chat" and obj.is_private:
            return is_follower(request, obj)
        else:
            return True
