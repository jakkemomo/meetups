from rest_framework import permissions

from apps.core.permissions.common import is_verified, is_owner, is_participant


class EventPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action == 'create':
            return is_verified(request)
        elif view.action in ['update', 'partial_update', 'destroy']:
            return is_verified(request) and is_owner(request, obj)
        elif view.action == 'register_for_event':
            return is_verified(request) and not is_participant(request, obj)
        elif view.action == 'leave_from_event':
            return is_verified(request) and is_participant(request, obj)
        elif view.action == 'add_to_favorite' or 'delete_from_favorite':
            return request.user.is_authenticated
        else:
            return False
