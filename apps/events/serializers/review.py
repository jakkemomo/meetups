from rest_framework import serializers

from apps.events.models import Review, Rating
from apps.events.serializers import RatingCreateSerializer, RatingUpdateSerializer, RatingRetrieveSerializer, \
    RatingListSerializer


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    rating = RatingRetrieveSerializer()

    class Meta:
        model = Review
        fields = ["review", "created_by", "event", 'rating']


class ReviewCreateSerializer(serializers.ModelSerializer):
    rating = RatingCreateSerializer()

    class Meta:
        model = Review
        fields = ["review", "rating"]

    def create(self, validated_data):
        user = self.context["request"].user
        event_id = self.context["view"].kwargs["event_id"]
        value = validated_data.get("rating")["value"]
        rating_default = {"value": value, "event_id": event_id, "user": user, 'created_by': user}
        rating_object = Rating.objects.update_or_create(defaults=rating_default, event_id=event_id, user=user)[0]
        review = validated_data["review"]
        review_object = Review.objects.create(review=review, created_by=user, event_id=event_id, rating=rating_object)
        return review_object


class ReviewUpdateSerializer(serializers.ModelSerializer):
    rating = RatingUpdateSerializer()

    class Meta:
        model = Review
        fields = ["review", 'rating', ]

    def update(self, instance, validated_data):
        instance.rating.value = validated_data.get("rating")["value"]
        instance.rating.updated_by = validated_data.get("rating")["user"]
        instance.review = validated_data.pop("review")
        instance.updated_by_id = self.context['request'].user.id
        instance.rating.save(force_update=True)
        instance.save()
        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    rating = RatingListSerializer()

    class Meta:
        model = Review
        fields = ["review", "created_by", "event", "rating"]
