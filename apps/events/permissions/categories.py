from rest_framework import permissions

from apps.core.permissions.common import is_verified


class CategoriesPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_verified(request) and request.user.is_staff
