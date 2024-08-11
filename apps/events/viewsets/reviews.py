from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.events.models import Review
from apps.events.permissions import ReviewPermissions
from apps.events.serializers import (
    EmptySerializer,
    ReviewCreateSerializer,
    ReviewListSerializer,
    ReviewResponseSerializer,
    ReviewRetrieveSerializer,
    ReviewUpdateSerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    model = Review
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewPermissions]
    lookup_url_kwarg = "review_id"
    http_method_names = ["post", "get", "put", "delete", "patch"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()
        return Review.objects.filter(event_id=self.kwargs["event_id"])

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return ReviewRetrieveSerializer
            case "create":
                return ReviewCreateSerializer
            case "update":
                return ReviewUpdateSerializer
            case "list":
                return ReviewListSerializer
            case "response_to_review":
                return ReviewResponseSerializer
            case _:
                return EmptySerializer

    @action(
        methods=["patch"],
        detail=True,
        url_path="response",
        url_name="review_response",
        permission_classes=[ReviewPermissions],
    )
    def response_to_review(self, request, review_id, event_id):
        review = self.get_object()
        review.response = request.data.get("response")
        review.save()
        serializer = ReviewRetrieveSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
