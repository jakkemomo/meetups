import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.core.utils import delete_image_if_exists, validate_city
from apps.profiles.models import UserRating, User
from apps.profiles.permissions import UserRatingPermissions, ProfilePermissions
from apps.profiles.serializers import (
    UserRatingListSerializer,
    UserRatingUpdateSerializer,
    UserRatingCreateSerializer,
    UserRatingRetrieveSerializer,
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
)

logger = logging.getLogger("profiles_app")


class UserRatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing user's ratings.
    """
    model = UserRating
    lookup_url_kwarg = 'rating_id'
    permission_classes = [IsAuthenticatedOrReadOnly, UserRatingPermissions]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        """
        This view should return a list of all the ratings for the user
        defined in user_id position of the URL
        """
        if getattr(self, "swagger_fake_view", False):
            return UserRating.objects.none()
        return UserRating.objects.filter(user_rated_id=self.kwargs["user_id"])

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return UserRatingRetrieveSerializer
            case "create":
                return UserRatingCreateSerializer
            case "update":
                return UserRatingUpdateSerializer
            case "list":
                return UserRatingListSerializer


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
        delete_image_if_exists(profile_instance)
        return super().destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        instance = self.get_object()
        city = self.request.data.get("city", None)
        if city:
            new_city = validate_city(city)
            if instance.city != new_city:
                instance.city = new_city
                instance.save()
        serializer.save()

class MyProfileViewSet(generics.RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileRetrieveSerializer

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: ProfileRetrieveSerializer,
        },
        tags=['profiles'],
    )
    def get(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
