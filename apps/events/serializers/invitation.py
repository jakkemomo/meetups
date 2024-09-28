from rest_framework import serializers

from apps.events.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="sender.username", read_only=True)
    image_url = serializers.CharField(source="sender.image_url", read_only=True)

    class Meta:
        model = Invitation
        fields = ("sender", "recipient", "status", "event_url", "username", "image_url")
