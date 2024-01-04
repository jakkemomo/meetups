
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.profiles.serializers import (
    UserRatingListSerializer,
    UserRatingUpdateSerializer,
    UserRatingCreateSerializer,
    UserRatingRetrieveSerializer,
)
from apps.profiles.permissions import UserRatingPermissions
from apps.profiles.models import UserRating


class UserRatingViewSet (viewsets.ModelViewSet):
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
