from rest_framework import serializers

from apps.profiles.models.followers import Follower


class FollowingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    image_url = serializers.CharField(source="user.image_url", read_only=True)

    class Meta:
        model = Follower
        fields = ("user", "follower", "status", "username", "image_url")
