import json
import logging
from uuid import uuid4

from django.core.serializers import serialize
from django.db.models import Q, Count, Avg
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, \
    IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.utils import delete_image_if_exists
from apps.events.filters import TrigramSimilaritySearchFilter, EventFilter
from apps.events.models import Event, Rating, Tag, FavoriteEvent, Category, Review, Currency
from apps.events.permissions import RatingPermissions, EventPermissions, TagPermissions, CategoriesPermissions, \
    ReviewPermissions
from apps.events.serializers import (
    EventListSerializer,
    EventRetrieveSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
    RatingCreateSerializer,
    RatingRetrieveSerializer,
    RatingUpdateSerializer,
    RatingListSerializer,
    TagCreateSerializer,
    TagRetrieveSerializer,
    TagUpdateSerializer,
    TagListSerializer,
    GeoJsonSerializer,
    EmptySerializer,
    ReviewRetrieveSerializer,
    ReviewCreateSerializer,
    ReviewUpdateSerializer,
    ReviewListSerializer,
    CategoryRetrieveSerializer, CategoryCreateSerializer,
    CategoryUpdateSerializer,
    CategoryListSerializer, CurrencyListSerializer,
)

logger = logging.getLogger("events_app")


class EventViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """

    def destroy(self, request, *args, **kwargs):
        event_instance = self.get_object()
        delete_image_if_exists(event_instance)
        # Proceed with the standard destroy operation
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        event_instance = self.get_object()
        if event_instance.image_url != request.data.get("image_url",
                                                        event_instance.image_url):
            delete_image_if_exists(event_instance)

        # Proceed with the standard update operation
        return super().update(request, *args, **kwargs)

    model = Event
    permission_classes = [IsAuthenticatedOrReadOnly, EventPermissions]
    filter_backends = [TrigramSimilaritySearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = EventFilter
    search_fields = ['name', 'description', 'address', 'tags__name', 'category__name', 'city']
    ordering_fields = ['start_date', 'average_rating', 'participants_number']
    lookup_url_kwarg = "event_id"

    def get_template_names(self):
        match self.action:
            case "retrieve":
                return ["events/detail.html"]
            case "list":
                return ["events/list.html"]
            case "create":
                return ["events/creation.html"]
            case "update":
                return ["events/edition.html"]
            case "partial_update":
                return ["events/edition.html"]
            case "destroy":
                return ["events/event_confirm_delete.html"]
            case "register_for_event":
                return ["events/detail.html"]
            case "leave_from_event":
                return ["events/detail.html"]

    def get_queryset(self):
        if self.kwargs.get("pk"):
            self.queryset = Event.objects.filter(id=self.kwargs["pk"])
        else:
            if self.request.user.id:
                self.queryset = self.model.objects.filter(
                    Q(is_visible=True) & Q(is_finished=False)
                    | Q(participants__in=[self.request.user.id]) & Q(is_finished=False)
                ).distinct()
            else:
                self.queryset = self.model.objects.filter(
                    Q(is_visible=True) & Q(is_finished=False)
                )
        return self.queryset.all().annotate(
            participants_number=Count("participants"),
            average_rating=Coalesce(Avg("ratings__value"), 0.0)
        )

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return EventRetrieveSerializer
            case "list":
                return EventListSerializer
            case "create":
                return EventCreateSerializer
            case "update":
                return EventUpdateSerializer
            case "partial_update":
                return EventUpdateSerializer
            case _:
                return EmptySerializer

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[EventPermissions],
        url_path="register",
        url_name="event_register",
    )
    def register_for_event(self, request, event_id: int):
        event = self.get_object()
        event.participants.add(request.user.id)
        event.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[EventPermissions],
        url_path="leave",
        url_name="event_leave",
    )
    def leave_from_event(self, request, event_id: int):
        event = self.get_object()
        event.participants.remove(request.user.id)
        event.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[EventPermissions],
        url_path='favorite',
        url_name='event_favorite_add'
    )
    def add_to_favorite(self, request, event_id: int):
        user_id = request.user.id
        favorite = FavoriteEvent(event_id=event_id, user_id=user_id)
        favorite.save()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body
    )
    @add_to_favorite.mapping.delete
    def delete_from_favorite(self, request, event_id: int):
        user_id = request.user.id
        FavoriteEvent.objects.filter(user_id=user_id, event_id=event_id).delete()
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='private-url',
        url_name='private_url',
        filter_backends=[],
        pagination_class=None
    )
    def set_private_url(self, request):
        private_url = str(uuid4())
        return Response(private_url, status=status.HTTP_200_OK)


class RatingViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event ratings.
    """

    model = Rating
    permission_classes = [IsAuthenticatedOrReadOnly, RatingPermissions, ]
    lookup_url_kwarg = "rating_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Rating.objects.none()
        self.queryset = Rating.objects.filter(event_id=self.kwargs["event_id"], user=self.request.user)
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


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event Categories.
    """

    model = Category
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, CategoriesPermissions]
    lookup_url_kwarg = "category_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return CategoryRetrieveSerializer
            case "create":
                return CategoryCreateSerializer
            case "update":
                return CategoryUpdateSerializer
            case "list":
                return CategoryListSerializer
            case _:
                return EmptySerializer

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly, CategoriesPermissions],
        url_path='favorite',
        url_name='category_favorite_add'
    )
    def add_category_to_favorite(self, request, category_id: int):
        user = request.user
        category = Category.objects.get(id=category_id)
        user.category_favorite.add(category)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=no_body
    )
    @add_category_to_favorite.mapping.delete
    def delete_category_from_favorite(self, request, category_id: int):
        user = request.user
        category = Category.objects.get(id=category_id)
        user.category_favorite.remove(category)
        return Response(status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event Tags.
    """

    model = Tag
    queryset = Tag.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, TagPermissions]
    lookup_url_kwarg = "tag_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return TagRetrieveSerializer
            case "create":
                return TagCreateSerializer
            case "update":
                return TagUpdateSerializer
            case "list":
                return TagListSerializer


class MarkerViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
    serializer_class = GeoJsonSerializer

    @swagger_auto_schema(
        tags=['map'],
        operation_description="Get all events in GeoJSON format",
    )
    def list(self, request, *args, **kwargs):
        geo_events = json.loads(
            serialize(
                "geojson", self.queryset.all(),
                geometry_field="location",
                fields=["id", "name", "start_date", "end_date", "description", "address"])
        )
        return Response(geo_events, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    model = Review
    permission_classes = [IsAuthenticatedOrReadOnly, ReviewPermissions]
    lookup_url_kwarg = "review_id"
    http_method_names = ["post", "get", "put", "delete"]

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


class CurrencyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Only get method is allowed for this viewset"""

    permission_classes = [AllowAny]
    queryset = Currency.objects.all()
    serializer_class = CurrencyListSerializer

    @swagger_auto_schema(
        tags=['currency'],
        operation_description="Get all currencies",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
