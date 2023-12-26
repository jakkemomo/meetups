from rest_framework import permissions

from apps.core.permissions.common import is_verified, is_participant


class UserRatingPermissions(permissions.BasePermission):
    """
    Object-level permission to only verified and participant user to edit another user of the event.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
#        elif view.action in ['create', 'update',]:
#            return is_verified(request) and is_participant(request, obj)
        else:
            return False
