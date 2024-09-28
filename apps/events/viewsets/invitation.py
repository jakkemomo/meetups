from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.events.models import Invitation, Event
from apps.events.serializers import InvitationSerializer
from apps.notifications.handlers.in_app import InAppNotificationsHandler
from apps.notifications.managers.chain import NotificationsChainManager
from apps.notifications.models import Notification
from apps.profiles.utils import get_user_object, is_current_user


class InvitationViewSet(viewsets.ModelViewSet):
    model = Invitation
    permission_classes = IsAuthenticated
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    http_method_names = ["get", "post", "delete"]

    handlers = (InAppNotificationsHandler(),)
    notifications_manager = NotificationsChainManager(handlers)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=["post"], detail=True, url_name="invite_accept")
    def invite_accept(self, request, event_id):
        event = Event.objects.filter(event_id=event_id).first()
        user = get_user_object(request.user.id)
        is_current_user(request, user)

        invitation_object = Invitation.objects.filter(event=event, recipient=user).first()

        if invitation_object.status == Invitation.status.ACCEPTED:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"detail": f"You are already participant of the {event}"},
            )
        invitation_object.status = Invitation.status.ACCEPTED
        invitation_object.save()
        serializer = self.get_serializer(invitation_object)

        self.notifications_manager.handle(
            created_by=invitation_object.sender,
            recipient=invitation_object.recipient,
            notification_type=Notification.Type.INVITE_TO_EVENT_ACCEPTED,
            additional_data={"invitation_status": invitation_object.status},
        )

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @swagger_auto_schema(request_body=no_body)
    @action(methods=["post"], detail=True, url_name="invite_reject")
    def invite_reject(self, request, event_id):
        event = Event.objects.filter(event_id=event_id).first()
        user = get_user_object(request.user.id)
        is_current_user(request, user)

        invitation_object = Invitation.objects.filter(event=event, recipient=user).first()
        if not invitation_object:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={"detail": f"You are do not have invitation to {event}"},
            )

        if invitation_object.status == Invitation.status.DECLINED:
            return Response(
                status=status.HTTP_409_CONFLICT,
                data={
                    "detail": f"You are rejected invitation {invitation_object} to event {event}"
                },
            )
        invitation_object.status = Invitation.status.DECLINED
        invitation_object.save()
        serializer = self.get_serializer(invitation_object)

        self.notifications_manager.handle(
            created_by=invitation_object.sender,
            recipient=invitation_object.recipient,
            notification_type=Notification.Type.INVITE_TO_EVENT_REJECTED,
            additional_data={"invitation_status": invitation_object.status},
        )

        return Response(status=status.HTTP_200_OK, data=serializer.data)
