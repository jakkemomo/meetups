from rest_framework import permissions

from apps.profiles.models.followers import Follower
from apps.profiles.utils import get_user_object, is_current_user


class FollowerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.action in [
            "list_followers",
            "list_following",
            "list_user_is_participant",
        ]:
            user = get_user_object(user_id=view.kwargs.get("user_id"))
            # TODO resolve user getting here and in endpoints
            # Maybe add this to request? But this is not explicit
            return (
                    is_current_user(request, user, raise_exception=False)
                    or
                    not user.is_private
                    or
                    user.is_private
                    and
                    Follower.objects.filter(
                        user=user,
                        follower=request.user,
                        status=Follower.Status.ACCEPTED,
                    ).exists()
            )
        else:
            return True