from rest_framework import permissions
from apps.core.permissions.common import is_verified


def is_reviewer(request, obj):
    return request.user == obj.user


class ReviewPermissions(permissions.BasePermission):
    """
    Object-level permission to only verified user to edit own review.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return is_verified(request) and is_reviewer(request, obj)
        else:
            return False
