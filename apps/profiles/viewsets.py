import logging

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.profiles.models import User
from apps.profiles.serializers import (
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
)
from apps.profiles.permissions import ProfilePermissions
from apps.core.utils import delete_image_if_exists


logger = logging.getLogger("profiles_app")


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ProfilePermissions, ]
    http_method_names = ["get", "put", "patch", "delete", ]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return ProfileRetrieveSerializer
            case "list":
                return ProfileListSerializer
            case "update":
                return ProfileUpdateSerializer
            case "partial_update":
                return ProfileUpdateSerializer

    def destroy(self, request, *args, **kwargs):
        profile_instance = self.get_object()
        result = delete_image_if_exists(profile_instance)
        if result:
            logger.warning(
                f"An error occurred while deleting a file: {result}"
            )

        return super().destroy(request, *args, **kwargs)
