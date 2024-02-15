from rest_framework import serializers

from apps.events.models import Review


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", ]

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        event_id = self.context["view"].kwargs["event_id"]
        review_object = Review.objects.create(review=validated_data["review"], user_id=user_id, event_id=event_id)
        return review_object


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", ]

    def update(self, instance, validated_data):
        review = validated_data.pop("review")
        instance.review = review
        instance.save()

        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "user", "event"]
