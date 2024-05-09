from asgiref.sync import async_to_sync
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.notifications.managers import NotificationManager
from apps.notifications.models import Notification
from apps.profiles.models.followers import Follower
from apps.profiles.permissions.followers import FollowerPermissions
from apps.profiles.serializers import FollowerSerializer
from apps.profiles.utils import get_user_object, is_current_user


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

        follower_object: Follower = Follower.objects.filter(
            user=user,
            follower=request.user
        ).first()

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
            async_to_sync(NotificationManager.notification)(
                created_by=follower_object.follower,
                recipient=follower_object.user,
                notification_type=Notification.Type.NEW_FOLLOW_REQUEST,
                additional_data={"follower_status": follower_object.status},
            )
        else:
            async_to_sync(NotificationManager.notification)(
                created_by=follower_object.follower,
                recipient=follower_object.user,
                notification_type=Notification.Type.NEW_FOLLOWER,
                additional_data={"follower_status": follower_object.status},
            )

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

        follower_object = Follower.objects.filter(
            user=request.user,
            follower=user
        ).first()

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

        async_to_sync(NotificationManager.notification)(
            created_by=follower_object.user,
            recipient=follower_object.follower,
            notification_type=Notification.Type.ACCEPTED_FOLLOW_REQUEST,
            additional_data={"follower_status": follower_object.status},
        )

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
