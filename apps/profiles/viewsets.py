
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
from apps.profiles.models import UserRating


class UserRatingViewSet (viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing user's ratings.
    """
    model = UserRating
    queryset = UserRating.objects.all()
    lookup_field = 'user_rated'
    permission_classes = [IsAuthenticatedOrReadOnly, UserRatingPermissions]
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if self.kwargs.get("pk"):
            self.queryset = UserRating.objects.filter(user_rated=self.kwargs["pk"])
        else:
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

    def list(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = UserRatingListSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)
