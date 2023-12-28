
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.profiles.serializers import (
    UserRatingListSerializer,
    UserRatingUpdateSerializer,
    UserRatingCreateSerializer,
    UserRatingRetrieveSerializer,
)
from apps.profiles.permissions import UserRatingPermissions
from apps.profiles.models import UserRating, User


class UserRatingViewSet (viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing user's ratings.
    """
    model = UserRating
    queryset = UserRating.objects.all()
    lookup_url_kwarg  = 'rating_id'
    permission_classes = [IsAuthenticatedOrReadOnly, UserRatingPermissions]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.kwargs.get("rating_id"):
            user = User.objects.filter(id=self.kwargs["user_id"])
            self.queryset = UserRating.objects.filter(user=user, user_rating=self.kwargs["rating_id"])
        else:
            user = User.objects.filter(id=self.kwargs["user_id"])
            self.queryset = UserRating.objects.filter(user_rated=self.request.user.id)
        return self.queryset.all()

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
