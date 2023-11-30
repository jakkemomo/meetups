from rest_framework import permissions


class EventPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if view.action in ('retrieve', 'list'):
            return True
        elif view.action == 'create':
            return request.user.is_authenticated and request.user.is_email_verified
        elif view.action in ['update', 'partial_update', 'destroy']:
            return request.user.is_staff or self.is_owner(request, obj)
        elif view.action == 'register_for_event':
            return not self.is_participant(request, obj)
        elif view.action == 'leave_from_event':
            return self.is_participant(request, obj)
        else:
            return False

    def is_participant(self, request, obj):
        return (
                request.user.is_authenticated and
                # request.user.is_email_verified and
                request.user != obj.created_by and
                request.user in obj.participants.all()
        )

    def is_owner(self, request, obj):
        return (
                request.user.is_authenticated and
                request.user == obj.created_by
        )
