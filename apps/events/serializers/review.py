from rest_framework import serializers

from apps.events.models import Review


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]

    def create(self, validated_data):
        user = self.context["request"].user
        review = validated_data.pop("review")
        event = self.context["request"].event_id
        rating_object = Review.objects.create(event=event, user=user, review=review)

        return rating_object


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]

    def update(self, instance, validated_data):
        review = validated_data.pop("review")
        instance.review = review
        instance.save()

        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]
