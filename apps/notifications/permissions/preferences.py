from rest_framework import permissions


class NotificationsPreferencesPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return is_preferences_owner(request, obj)


def is_preferences_owner(request, obj):
    return request.user == obj.user
