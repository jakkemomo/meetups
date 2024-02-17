from rest_framework import serializers

from apps.events.models import Review


class ReviewRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "created_by", "event"]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", ]

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        event_id = self.context["view"].kwargs["event_id"]
        review_object = Review.objects.create(review=validated_data["review"], created_by_id=user_id, event_id=event_id)
        return review_object


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", ]

    def update(self, instance, validated_data):
        instance.review = validated_data.pop("review")
        instance.updated_by_id = self.context['request'].user.id
        instance.save()
        return instance


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["review", "created_by", "event"]
