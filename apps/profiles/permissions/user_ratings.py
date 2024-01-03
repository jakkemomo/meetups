from rest_framework import permissions
from apps.core.permissions.common import is_verified, is_owner


class UserRatingPermissions(permissions.BasePermission):
    """
    Object-level permission to only verified user to edit another user rating and not allow edit own rating.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return is_verified(request) and is_not_rated(request, obj) and is_owner(request, obj)
        else:
            return False


def is_not_rated(request, obj):
    return request.user != obj.user_rated or request.user.is_staff
