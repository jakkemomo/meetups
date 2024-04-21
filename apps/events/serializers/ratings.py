from rest_framework import serializers

from apps.events.models import Event, Rating


class RatingCreateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0, max_value=10, default=10)

    class Meta:
        model = Rating
        fields = ["value", "user"]


class RatingRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ["value", "user"]


class RatingUpdateSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(min_value=0, max_value=10, default=10)

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
