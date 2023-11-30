from rest_framework import permissions


class RatingPermissions(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        is_participant = (
                request.user.is_authenticated and
                request.user.is_email_verified and
                request.user != obj.created_by and
                request.user in obj.participants.all() and
                obj.is_finished
        )

        if view.action in ('retrieve', 'list'):
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return is_participant
        else:
            return False
