import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.utils import delete_image_if_exists
from apps.profiles.models import User
from apps.profiles.permissions import ProfilePermissions
from apps.profiles.serializers import (
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
)

logger = logging.getLogger("profiles_viewsets")


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ProfilePermissions, ]
    http_method_names = ["get", "put", "patch", "delete", ]
    lookup_url_kwarg = "user_id"

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
        delete_image_if_exists(profile_instance)
        return super().destroy(request, *args, **kwargs)


class MyProfileViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileRetrieveSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProfileRetrieveSerializer,
        },
        tags=['users'],
    )
    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
