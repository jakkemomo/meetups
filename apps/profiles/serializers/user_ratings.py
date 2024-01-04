from rest_framework import serializers
from apps.profiles.models.user_rate import UserRating


class UserRatingCreateSerializer(serializers.ModelSerializer):
    """
    User's rating serializers for profile viewset
    """
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'comment']

    def create(self, validated_data):
        validated_data['created_by_id'] = self.context["request"].user.id
        validated_data['user_rated_id'] = self.context["view"].kwargs["user_id"]
        user_rating = UserRating(**validated_data)
        user_rating.save()
        return user_rating


class UserRatingUpdateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'comment']


class UserRatingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        fields = ['value', 'created_by', 'comment']


class UserRatingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['value', 'comment']
