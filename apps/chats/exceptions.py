from rest_framework import status
from rest_framework.exceptions import APIException


class ChatWithoutEventException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class DirectChatUserNotFoundException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ChatTypeException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
