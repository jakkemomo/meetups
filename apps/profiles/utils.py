import logging

from apps.profiles.exceptions import (
    UserNotFoundException,
    UserAreCurrentException,
)
from apps.profiles.models import User
from apps.profiles.models.followers import Follower


logger = logging.getLogger(__name__)


def get_user_object(user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise UserNotFoundException
    return user


def is_current_user(request, user, raise_exception=True):
    if user == request.user:
        if raise_exception:
            raise UserAreCurrentException()
        return True
    return False


def change_followers_if_exists(user):
    try:
        (Follower.objects.filter(user=user, status=Follower.Status.PENDING)
         .update(status=Follower.Status.ACCEPTED))
        (Follower.objects.filter(user=user, status=Follower.Status.DECLINED)
         .delete())
    except Exception as exc:
        logger.error(
            f"An error occurred while changing followers of user: {user}.\n{exc}"
        )
        raise


def is_follower(request, user):
    return Follower.objects.filter(
                user=user,
                follower=request.user,
                status=Follower.Status.ACCEPTED,
            ).exists()
