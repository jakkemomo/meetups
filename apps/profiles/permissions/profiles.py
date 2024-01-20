from rest_framework import permissions


class ProfilePermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user == obj
        else:
            return False
