from django.utils.translation import gettext_lazy as _


from apps.profiles.exceptions import UserNotFoundException, \
    UserAreCurrentException
from apps.profiles.models import User


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
