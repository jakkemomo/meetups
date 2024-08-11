from rest_framework import serializers, viewsets
from rest_framework.response import Response

from apps.events.models import Event, Rating
from apps.events.permissions import RatingPermissions
from apps.events.serializers import (
    EmptySerializer,
    RatingCreateSerializer,
    RatingListSerializer,
    RatingRetrieveSerializer,
    RatingUpdateSerializer,
)


class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event ratings.
    """

    model = Rating
    permission_classes = [RatingPermissions]
    lookup_url_kwarg = "rating_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Rating.objects.none()
        self.queryset = Rating.objects.filter(
            event_id=self.kwargs["event_id"], user=self.request.user
        )
        return self.queryset.all()

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return RatingRetrieveSerializer
            case "create":
                return RatingCreateSerializer
            case "update":
                return RatingUpdateSerializer
            case "list":
                return RatingListSerializer
            case _:
                return EmptySerializer

    def list(self, request, *args, **kwargs):
        queryset = Rating.objects.filter(event_id=kwargs["event_id"])
        serializer = RatingListSerializer(queryset, many=True, context={"request": request})

        return Response(serializer.data)

    def perform_create(self, serializer):
        event = Event.objects.get(id=self.kwargs["event_id"])
        self.check_object_permissions(self.request, event)
        user = self.request.user
        if event.ratings.filter(user=user).exists():
            raise serializers.ValidationError("You have already rated this event")
        rating = serializer.save(
            user=self.request.user,
            event=event,
            created_by=self.request.user,
            value=serializer.validated_data["value"],
        )
        event.ratings.add(rating)
