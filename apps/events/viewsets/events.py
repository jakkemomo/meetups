import logging

from django.db.models import Q, Count, Avg, Exists, OuterRef
from django.db.models.functions import Coalesce
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.response import Response

from apps.core.utils import delete_image_if_exists
from apps.events.filters import TrigramSimilaritySearchFilter, EventFilter
from apps.events.models import Event, FavoriteEvent
from apps.events.permissions import EventPermissions
from apps.events.serializers import (
    EventRetrieveSerializer,
    EventListSerializer,
    EventCreateSerializer,
    EventUpdateSerializer,
    EmptySerializer,
)


class EventViewSet(viewsets.ModelViewSet):
    model = Event
    permission_classes = [IsAuthenticatedOrReadOnly, EventPermissions]
    filter_backends = [TrigramSimilaritySearchFilter, OrderingFilter, DjangoFilterBackend]
    filterset_class = EventFilter
    search_fields = ['name', 'description', 'address', 'tags__name', 'category__name',]
    ordering_fields = ['start_date', 'average_rating', 'participants_number']
    lookup_url_kwarg = "event_id"

    def get_queryset(self):
        if self.kwargs.get("event_id"):
            self.queryset = Event.objects.filter(id=self.kwargs["event_id"])
        elif self.kwargs.get("token"):
            self.queryset = Event.objects.filter(
                private_token=self.kwargs["token"]
            )
        else:
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
        queryset = self.queryset.prefetch_related('category', 'tags').annotate(
            participants_number=Count("participants"),
            average_rating=Coalesce(Avg("ratings__value"), 0.0),
            is_favorite=Exists(
                FavoriteEvent.objects.filter(
                    event_id=OuterRef("id"), user_id=self.request.user.id
                )
            ),
        ).order_by("-start_date")
        return queryset.all()

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
            case "get_private_event":
                return EventRetrieveSerializer
            case _:
                return EmptySerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response = Response(serializer.data)
        if self.kwargs.get('token'):
            response.set_cookie("private_event_key",
                                value=self.kwargs['token'],
                                expires=instance.end_date,
                                httponly=True)
        return response

    def destroy(self, request, *args, **kwargs):
        event_instance = self.get_object()
        delete_image_if_exists(event_instance)
        # Proceed with the standard destroy operation
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        event_instance = self.get_object()
        if event_instance.image_url != request.data.get(
                "image_url",
                event_instance.image_url
        ):
            delete_image_if_exists(event_instance)

        # Proceed with the standard update operation
        return super().update(request, *args, **kwargs)

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
        if event.type == 'private' and request.COOKIES.get('private_event_key') != event.private_token:
            return Response(status=status.HTTP_403_FORBIDDEN)
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
        request_body=no_body
    )
    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated, EventPermissions],
        url_path='private/(?P<token>[^/.]+)',
        url_name='private',
        lookup_url_kwarg="token",
        lookup_field='private_token'
    )
    def get_private_event(self, request, token):
        return self.retrieve(request, token)

    @swagger_auto_schema(
        request_body=no_body,
        tags=["events"]
    )
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[EventPermissions],
        url_path="kick/(?P<user_id>[^/.]+)",
        url_name="kick_from_event"
    )
    def kick_participant_from_event(self, request, event_id, user_id):
        event = self.get_object()
        event.participants.remove(user_id)
        event.save()
        return Response(status=status.HTTP_200_OK)
