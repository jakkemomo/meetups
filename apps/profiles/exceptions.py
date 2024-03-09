from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _


class UserNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _("User not found")


class UserAreCurrentException(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _("This is a current user")
