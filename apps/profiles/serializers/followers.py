from rest_framework import serializers

from apps.profiles.models.followers import Follower


class FollowerSerializer(serializers.ModelSerializer):
    queryset = Follower.objects.prefetch_related("followers", "users")

    class Meta:
        model = Follower
        depth = 1
        fields = (
            "user",
            "follower",
            "status",
        )

    def create(self, validated_data):
        user = validated_data.get("user")
        follower = validated_data.get("follower")
        return Follower.objects.create(
            user=user,
            follower=follower,
            status=Follower.Status.PENDING if user.is_private else Follower.Status.ACCEPTED,
        )
