from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from apps.profiles.models.user_rate import UserRating, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar_url"]


class UserRatingCreateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'user_rated', 'comment']

    def create(self, validated_data):
        user_rated = get_object_or_404(User, id=self.context["view"].kwargs["user_rated_id"])
        user_rater = self.context["request"].user_rater
        value = validated_data.pop("value")
        user_rating_object = UserRating.objects.create(user_rated=user_rated, user_rater=user_rater, value=value)

        return user_rating_object


class UserRatingUpdateSerializer(serializers.ModelSerializer):
    """
    User's rating serializer for profile viewset
    """
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'user_rated', 'comment']

    def update(self, instance, validated_data):
        value = validated_data.pop("value")
        instance.value = value
        instance.save()

        return instance


class UserRatingListSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = UserRating
        fields = ['value', 'user_rater', 'user_rated', 'comment']


class UserRatingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['value', 'user_rated', 'comment']
