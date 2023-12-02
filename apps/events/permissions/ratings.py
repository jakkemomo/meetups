from rest_framework import permissions

from apps.events.permissions.common import is_participant, is_verified


class RatingPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if view.action in ('retrieve', 'list'):
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return is_verified(request) and is_participant(request, obj) and obj.is_finished
        else:
            return False
