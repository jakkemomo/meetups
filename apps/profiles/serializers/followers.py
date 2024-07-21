from rest_framework import serializers

from apps.profiles.models.followers import Follower


class FollowerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="follower.username", read_only=True)
    image_url = serializers.CharField(source="follower.image_url", read_only=True)

    class Meta:
        model = Follower
        fields = (
            "user",
            "follower",
            "status",
            "username",
            "image_url",
        )

    def create(self, validated_data):
        user = validated_data.get("user")
        follower = validated_data.get("follower")
        return Follower.objects.create(
            user=user,
            follower=follower,
            status=Follower.Status.PENDING if user.is_private else Follower.Status.ACCEPTED,
        )
