from rest_framework import permissions


class TagPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve', 'list'):
            return True
        elif view.action == 'create':
            return request.user.is_staff
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff
        else:
            return False
