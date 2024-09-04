from rest_framework import serializers

from apps.events.models.invitations import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ["event", "recipient"]
