from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from apps.profiles.models.user_rate import UserRating, User


class UserRatingCreateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'comment']

    def create(self, validated_data):
        user = get_object_or_404(User, id=self.context["view"].kwargs["user_id"])
        creator = self.context["request"].user
        value = validated_data.pop("value")
        user_rating = UserRating.objects.create(user_rated=user, value=value, created_by=creator)
        return user_rating


class UserRatingUpdateSerializer(serializers.ModelSerializer):
    """
    User's rating serializer for profile viewset
    """
    value = serializers.IntegerField(min_value=0, max_value=5, default=5)

    class Meta:
        model = UserRating
        fields = ['value', 'comment']

    def update(self, instance, validated_data):
        value = validated_data.pop("value")
        comment = validated_data.pop("comment")
        updater = self.context["request"].user
        instance.value = value
        instance.comment = comment
        instance.updated_by = updater
        instance.save()

        return instance


class UserRatingListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserRating
        fields = ['value', 'created_by', 'comment']


class UserRatingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ['value', 'comment']
