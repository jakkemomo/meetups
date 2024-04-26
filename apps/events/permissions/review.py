from rest_framework import permissions
from apps.core.permissions.common import is_verified, is_owner, is_participant


class ReviewPermissions(permissions.BasePermission):
    """
    Object-level permission to only verified user to edit own review.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action in ['update', 'destroy']:
            return is_verified(request) and is_participant(request, obj)
        elif view.action in ['partial_update',]:
            return is_verified(request) and is_owner(request, obj.event)
        else:
            return False
