from uuid import uuid4

from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.events.models import Event, Tag, Category, Schedule, Currency
from apps.profiles.models import User


class LocationSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_digits=7, decimal_places=5, write_only=True)
    longitude = serializers.DecimalField(max_digits=7, decimal_places=5, write_only=True)

    class Meta:
        model = Event
        fields = ["latitude", "longitude"]

    def to_representation(self, value):
        return {
            "latitude": value.y,
            "longitude": value.x
        }


class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.ChoiceField(choices=Schedule.DayOfWeek.choices, required=True)
    time = serializers.TimeField(required=True)

    class Meta:
        model = Schedule
        fields = ["day_of_week", "time"]


class EventCreateSerializer(serializers.ModelSerializer):
    desired_participants_number = serializers.IntegerField(min_value=0, max_value=10000000, default=1)
    location = LocationSerializer(required=True, many=False)
    city_south_west_point = LocationSerializer(required=True, many=False)
    city_north_east_point = LocationSerializer(required=True, many=False)
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    cost = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True, required=False)
    repeatable = serializers.BooleanField(default=False)
    participants_age = serializers.IntegerField(min_value=0, max_value=100, default=18)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), required=False)
    free = serializers.BooleanField(default=True)
    gallery = serializers.ListField(child=serializers.CharField(max_length=250), allow_empty=True, required=False,
                                    default=[])
    schedule = ScheduleSerializer(many=True, required=False, allow_empty=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False, default=[])
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    is_finished = serializers.BooleanField(default=False)
    is_visible = serializers.BooleanField(default=True)
    any_participant_number = serializers.BooleanField(default=False)
    start_time = serializers.TimeField(required=True)
    end_time = serializers.TimeField(required=False)

    class Meta:
        model = Event
        exclude = ["participants", "created_by", "updated_by"]

    def create(self, validated_data):
        validated_data["location"] = Point(
            (
                validated_data["location"]["longitude"],
                validated_data["location"]["latitude"]
            )
        )
        validated_data["city_south_west_point"] = Point(
            (
                validated_data["city_south_west_point"]["longitude"],
                validated_data["city_south_west_point"]["latitude"]
            )

        )
        validated_data["city_north_east_point"] = Point(
            (
                validated_data["city_north_east_point"]["longitude"],
                validated_data["city_north_east_point"]["latitude"]
            )
        )
        request = self.context["request"]
        user_id = request.user.id
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id
        tags = validated_data.pop("tags")
        schedule = validated_data.pop("schedule", [])
        if validated_data["type"] == "private":
            validated_data["private_url"] = uuid4()
        event = Event(**validated_data)
        event.save()
        for schedule_data in schedule:
            new_schedule = Schedule.objects.create(event=event, **schedule_data)
            event.schedule.add(new_schedule)
        if tags:
            event.tags.set([tag.id for tag in tags])
        return event

    # def to_representation(self, instance):
    #     instance.location = instance.location.geojson
    #     instance.city_south_west_point = instance.city_south_west_point.geojson
    #     instance.city_north_east_point = instance.city_north_east_point.geojson
    #     instance = super().to_representation(instance)
    #     return instance


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
        event_type = validated_data.pop("type")
        if event_type == "private":
            instance.private_url = uuid4()
        else:
            instance.private_url = None
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
    participants_number = serializers.IntegerField()

    def get_location(self, obj):
        if not obj.location:
            return None
        return obj.location.coords

    class Meta:
        model = Event
        exclude = ["ratings", "updated_by", "city_south_west_point", "city_north_east_point"]


class EmptySerializer(serializers.Serializer):
    pass
