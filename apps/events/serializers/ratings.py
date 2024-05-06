from rest_framework import serializers

from apps.events.models import Rating


class RatingCreateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=1, max_value=5, default=5)

    class Meta:
        model = Rating
        fields = ["value", "user"]


class RatingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["value", "user"]


class RatingUpdateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=1, max_value=5, default=5)

    class Meta:
        model = Rating
        fields = ["value", "user"]

    def update(self, instance, validated_data):
        value = validated_data.pop("value")
        instance.value = value
        instance.save()

        return instance


class RatingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["value", "user", "event"]
