from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("User not found")


class UserAreCurrentException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("This is a current user")


class FollowersChangingException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
