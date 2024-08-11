from rest_framework import permissions

from apps.core.permissions.common import is_owner, is_participant, is_verified


def has_access_to_private(request, obj):
    token_pass = request.parser_context.get("kwargs").get("token") == obj.private_token
    return token_pass or is_participant(request, obj) or is_owner(request, obj)


class EventPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action == "create":
            return is_verified(request)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.type == "private" and not has_access_to_private(request, obj):
                return False
            return True
        elif view.action in ["update", "partial_update", "destroy", "kick_participant_from_event"]:
            return is_verified(request) and is_owner(request, obj)
        elif view.action == "register_for_event":
            return is_verified(request) and not is_participant(request, obj)
        elif view.action == "leave_from_event":
            return is_verified(request) and is_participant(request, obj)
        elif view.action == "add_to_favorite" or "delete_from_favorite":
            return request.user.is_authenticated
        else:
            return False
