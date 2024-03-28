from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.core.utils import validate_city
from apps.events.models import Event, Tag, Category
from apps.events.utils import Currency
from apps.profiles.models import User
from apps.profiles.serializers.cities import CityRetrieveSerializer, CityUpdateSerializer


class EventCreateSerializer(serializers.ModelSerializer):
    desired_participants_number = serializers.IntegerField(min_value=0, max_value=10000000, default=1)
    location = serializers.ListField(
        child=serializers.DecimalField(max_digits=7, decimal_places=5), max_length=2, min_length=2
    )
    city = CityUpdateSerializer(many=False, required=True)

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
        city = validate_city(validated_data.pop("city"))
        event = Event(**validated_data, city_id=city.id)
        event.save()
        if tags:
            event.tags.set([tag.id for tag in tags])
        return event

    def to_representation(self, instance):
        instance.location = instance.location.geojson
        instance = super().to_representation(instance)
        return instance


class EventUpdateSerializer(EventCreateSerializer):
    desired_participants_number = serializers.IntegerField(
        min_value=0, max_value=10000000, allow_null=True, required=False
    )
    location = serializers.ListField(
        child=serializers.DecimalField(max_digits=7, decimal_places=5),
        max_length=2,
        min_length=2,
        required=False,
    )

    # todo: move serializer logic to services

    def update(self, instance, validated_data):
        location = validated_data.pop("location", None)
        if location:
            instance.location = Point(location)
        tags = validated_data.pop("tags", None)
        if tags:
            instance.tags.set([tag.id for tag in tags])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "image_url"]


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
    category = EventCategorySerializer(many=False)
    participants_number = serializers.IntegerField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "rating",
            "image_url",
            "description",
            "start_date",
            "end_date",
            "tags",
            "address",
            "category",
            "participants_number",
        ]


class EventRetrieveSerializer(BaseEventSerializer):
    participants = ParticipantSerializer(many=True)
    tags = EventTagSerializer(many=True)
    category = EventCategorySerializer(many=False)
    created_by = ParticipantSerializer(many=False)
    location = serializers.SerializerMethodField("get_location")
    city = CityRetrieveSerializer(many=False)
    participants_number = serializers.IntegerField()

    def get_location(self, obj):
        if not obj.location:
            return None
        return obj.location.coords

    class Meta:
        model = Event
        exclude = ["ratings", "updated_by"]


class EmptySerializer(serializers.Serializer):
    pass
