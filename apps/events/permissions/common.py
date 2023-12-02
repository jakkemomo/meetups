from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.created_by == request.user


def is_participant(request, obj):
    return (
            request.user != obj.created_by and
            request.user in obj.participants.all()
    )


def is_owner(request, obj):
    return request.user == obj.created_by or request.user.is_staff


def is_verified(request):
    return request.user.is_authenticated and request.user.is_email_verified
