from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.events.models import Event, Tag, Category
from apps.profiles.models import User


class EventCreateSerializer(serializers.ModelSerializer):
    current_participants_number = serializers.IntegerField(min_value=0, max_value=10000)
    desired_participants_number = serializers.IntegerField(min_value=0, max_value=10000)
    location = serializers.ListField(
        child=serializers.DecimalField(max_digits=7, decimal_places=5), max_length=2, min_length=2
    )

    class Meta:
        model = Event
        exclude = ["participants", "created_by", "updated_by"]

    def create(self, validated_data):
        validated_data["location"] = Point(validated_data.pop("location"))
        request = self.context["request"]
        user_id = request.user.id
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        tags = validated_data.pop("tags")
        event = Event(**validated_data)
        event.save()
        event.tags.set([tag.id for tag in tags])
        return event

    def update(self, instance, validated_data):
        if validated_data.get("location"):
            instance.location = Point(validated_data.pop("location"))
        return instance

    def to_representation(self, instance):
        instance.location = instance.location.geojson
        instance = super().to_representation(instance)
        return instance


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class EventTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BaseEventSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField("get_rating")

    def get_rating(self, obj):
        ratings = obj.ratings.through.objects.filter(event=obj).values_list("value", flat=True)
        if not ratings:
            return None
        return sum(ratings) / len(ratings)


class EventListSerializer(BaseEventSerializer):
    tags = EventTagSerializer(many=True)

    class Meta:
        model = Event
        fields = ["id", "name", "rating", "image", "description", "start_date", "end_date", "tags"]


class EventRetrieveSerializer(BaseEventSerializer):
    participants = ParticipantSerializer(many=True)
    tags = EventTagSerializer(many=True)
    category = EventCategorySerializer(many=False)
    created_by = ParticipantSerializer(many=False)
    location = serializers.SerializerMethodField("get_location")

    def get_location(self, obj):
        if not obj.location:
            return None
        return obj.location.coords

    class Meta:
        model = Event
        exclude = ["ratings", "updated_by"]
