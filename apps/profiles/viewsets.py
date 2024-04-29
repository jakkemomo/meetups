import logging

from django.db.models import Count, Avg, Q
from django.db.models.functions import Coalesce
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.core.utils import delete_image_if_exists
from apps.events.models import Event, FavoriteEvent
from apps.events.serializers import EventListSerializer
from apps.profiles.managers import NotificationManager
from apps.profiles.models import UserRating, User
from apps.profiles.models.followers import Follower
from apps.profiles.permissions import (
    UserRatingPermissions,
    ProfilePermissions,
)
from apps.profiles.permissions.followers import FollowerPermissions
from apps.profiles.serializers import (
    UserRatingListSerializer,
    UserRatingUpdateSerializer,
    UserRatingCreateSerializer,
    UserRatingRetrieveSerializer,
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    ProfileListSerializer,
    FollowerSerializer,
)
from apps.profiles.utils import get_user_object, is_current_user
from django.db.models import Subquery
from django.utils import timezone

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


class FollowerViewSet(viewsets.ModelViewSet):
    model = Follower
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = (IsAuthenticated, FollowerPermissions)
    http_method_names = ["get", "post", "delete"]
    lookup_url_kwarg = "user_id"

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=["post"],
        detail=True,
        url_name="follow_user",
    )
    def follow(self, request, user_id):
        user = get_user_object(user_id=user_id)
        is_current_user(request, user)

        follower_object = Follower.objects.filter(user=user, follower=request.user).first()
        if follower_object:
            if follower_object.status == Follower.Status.ACCEPTED:
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={"detail": "Already following"}
                )
            elif follower_object.status in (
                    Follower.Status.PENDING,
                    Follower.Status.DECLINED,
            ):
                return Response(
                    status=status.HTTP_409_CONFLICT,
                    data={"detail": "Follow request already sent"}
                )

        data = {"user": user.id, "follower": request.user.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        follower_object = serializer.save()

        if user.is_private:
            NotificationManager.follow_request(follower_object=follower_object)
        else:
            NotificationManager.follow(follower_object=follower_object)

        return Response(
            status=status.HTTP_201_CREATED,
            data=serializer.data,
        )

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=["post"],
        detail=True,
        url_name="accept_follow_request",
    )
    def accept(self, request, user_id):
        user = get_user_object(user_id=user_id)
        is_current_user(request, user)

        follower_object = Follower.objects.filter(user=request.user, follower=user, ).first()
        if not follower_object:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": "No such follow requests was found"}
            )

        if follower_object.status == Follower.Status.ACCEPTED:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"detail": f"{user} is already following you"},
            )

        follower_object.status = Follower.Status.ACCEPTED
        follower_object.save()
        serializer = self.get_serializer(follower_object)

        NotificationManager.accept_follow_request(follower_object=follower_object)

        return Response(
            status=status.HTTP_200_OK,
            data=serializer.data,
        )

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=["delete"],
        detail=True,
        url_name="unfollow_user",
    )
    def unfollow(self, request, user_id):
        user = get_user_object(user_id=user_id)
        is_current_user(request, user)

        follower_object = Follower.objects.filter(user=user, follower=request.user).first()
        if not follower_object:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"detail": f"You are not following {user}"},
            )

        if follower_object.status == Follower.Status.ACCEPTED:
            message = f"You are no longer following {user}"
        else:
            message = f"You canceled follow request to {user}"

        follower_object.delete()

        return Response(
            status=status.HTTP_200_OK,
            data={"detail": message},
        )

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=["get"],
        detail=True,
        url_path="followers",
        url_name="list_user_followers",
    )
    def list_followers(self, request, user_id):
        user = get_user_object(user_id=user_id)
        queryset = self.queryset.filter(user=user, status=Follower.Status.ACCEPTED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(
        request_body=no_body,
    )
    @action(
        methods=["get"],
        detail=True,
        url_path="following",
        url_name="list_user_following",
    )
    def list_following(self, request, user_id):
        user = get_user_object(user_id=user_id)
        queryset = self.queryset.filter(follower=user, status=Follower.Status.ACCEPTED)
        serializer = self.get_serializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class ProfileEventViewSet(viewsets.ModelViewSet):
    model = Event
    serializer_class = EventListSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthenticated,
        FollowerPermissions,
    ]
    http_method_names = ["get"]
    lookup_url_kwarg = "user_id"

    def get_queryset(self):
        self.queryset = (
            self.model.objects
            .annotate(
                participants_number=Count("participants"),
                average_rating=Coalesce(Avg("ratings__value"), 0.0)
            )
            .filter(
                Q(is_visible=True) & Q(type="open") |
                Q(participants__in=[self.request.user.id]) & Q(type="private") |
                Q(created_by=self.request.user) & Q(type="private")
            )
            .order_by("-start_date")
        )
        return self.queryset.all()

    @swagger_auto_schema(
        request_body=no_body
    )
    @action(
        methods=["get"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly],
        url_path="events/created_by",
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
        detail=True,
        permission_classes=[IsAuthenticated, FollowerPermissions],
        url_path="events/is_participant",
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
        url_path="events/favorite_events",
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
        url_path="events/finished_events",
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
        url_path="events/planned_events",
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
