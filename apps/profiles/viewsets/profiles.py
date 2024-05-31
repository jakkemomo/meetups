from django.db.models import Q, Count, Avg, Exists, OuterRef, Subquery
from django.db.models.functions import Coalesce
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend

from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, \
    IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter

from apps.core.utils import delete_image_if_exists
from apps.events.models import Event, FavoriteEvent
from apps.events.serializers import EventListSerializer
from apps.events.filters import TrigramSimilaritySearchFilter, EventFilter
from apps.profiles.models import User
from apps.profiles.permissions import ProfilePermissions
from apps.profiles.permissions.followers import FollowerPermissions
from apps.profiles.serializers import (
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
)
from apps.profiles.utils import get_user_object


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


class ProfileEventViewSet(viewsets.ModelViewSet):
    model = Event
    serializer_class = EventListSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthenticated,
        FollowerPermissions,
    ]
    filter_backends = [TrigramSimilaritySearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = EventFilter
    search_fields = ['name', 'description', 'address', 'tags__name', 'category__name', 'city']
    ordering_fields = ['start_date', 'average_rating', 'participants_number']
    http_method_names = ["get"]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        if self.request.user.id:
            self.queryset = self.model.objects.filter(
                Q(is_visible=True) &
                Q(is_finished=False) & (
                        Q(type="open") |
                        Q(participants__in=[self.request.user.id]) & Q(type="private") |
                        Q(created_by=self.request.user) & Q(type="private")
                )
            )
        else:
            self.queryset = self.model.objects.filter(
                Q(is_visible=True) & Q(is_finished=False) & Q(type="open")
            )

        self.queryset = self.queryset.prefetch_related('category',
                                                       'tags').annotate(
            participants_number=Count("participants"),
            average_rating=Coalesce(Avg("ratings__value"), 0.0),
            is_favorite=Exists(
                FavoriteEvent.objects.filter(
                    event_id=OuterRef("id"), user_id=self.request.user.id
                )
            ),
        ).order_by("-start_date")
        return self.queryset.all()

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="events/created",
        url_name="event_list_created_by_user",
    )
    def list_created_by_user(self, request, user_id):
        user = get_user_object(user_id)
        queryset = self.get_queryset().filter(created_by=user)

        if user != request.user:
            queryset = queryset.filter(is_visible=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated, FollowerPermissions],
        url_path='(?P<user_id>[^/.]+)/events/participants',
        url_name="event_list_user_is_participant",
    )
    def list_user_is_participant(self, request, user_id):
        user = get_user_object(user_id)
        queryset = self.get_queryset().filter(participants__id=user_id)

        if user != request.user:
            queryset = queryset.filter(is_visible=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="events/favorited",
        url_name="user_favorite_events",
    )
    def list_user_favorite_events(self, request, user_id):
        queryset = self.get_queryset().filter(id__in=Subquery(
            FavoriteEvent.objects.filter(user_id=user_id).values('event_id')))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="events/finished",
        url_name="user_finished_events",
    )
    def list_user_finished_events(self, request, user_id):
        queryset = self.get_queryset().filter(participants__id=user_id, end_date__lt=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticated],
        url_path="events/planned",
        url_name="user_planned_events",
    )
    def list_user_planned_events(self, request, user_id):
        queryset = self.get_queryset().filter(participants__id=user_id, start_date__gt=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(auto_schema=None)
    def retrieve(self, request):
        pass

    @swagger_auto_schema(auto_schema=None)
    def list(self, request):
        pass
