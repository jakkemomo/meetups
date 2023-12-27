from rest_framework import permissions



class UserRatingPermissions(permissions.BasePermission):
    """
    Object-level permission to only verified and participant user to edit another user of the event.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False
