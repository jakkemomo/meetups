from uuid import uuid4

from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.events.models import Event, Tag, Category, Schedule, Currency
from apps.profiles.models import User
from apps.chats.models import Chat


class LocationSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(max_value=180, min_value=-180,
                                        write_only=True, max_digits=18, decimal_places=15)
    longitude = serializers.DecimalField(max_value=180, min_value=-180,
                                         write_only=True, max_digits=18, decimal_places=15)

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
    desired_participants_number = serializers.IntegerField(min_value=0, max_value=10000000, default=0, allow_null=True,
                                                           required=False)
    location = LocationSerializer(required=True, many=False)
    city_south_west_point = LocationSerializer(required=True, many=False)
    city_north_east_point = LocationSerializer(required=True, many=False)
    city = serializers.CharField(max_length=50)
    country = serializers.CharField(max_length=50)
    cost = serializers.DecimalField(max_digits=8, decimal_places=2, allow_null=True, required=False)
    repeatable = serializers.BooleanField(default=False)
    participants_age = serializers.IntegerField(min_value=0, max_value=100, default=18)
    currency = serializers.PrimaryKeyRelatedField(queryset=Currency.objects.all(), required=False, allow_null=True,
                                                  default=None)
    free = serializers.BooleanField(default=True)
    gallery = serializers.ListField(child=serializers.CharField(max_length=250), allow_empty=True, required=False)
    schedule = ScheduleSerializer(many=True, required=False, allow_empty=True, allow_null=True)
    tags = serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all(), required=False, allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)
    is_finished = serializers.BooleanField(default=False)
    is_visible = serializers.BooleanField(default=True)
    any_participant_number = serializers.BooleanField(default=False)

    start_date = serializers.DateField(required=False, allow_null=True, default=None)
    end_date = serializers.DateField(required=False, allow_null=True, default=None)
    start_time = serializers.TimeField(required=False, allow_null=True, default=None)
    end_time = serializers.TimeField(required=False, allow_null=True, default=None)

    class Meta:
        model = Event
        exclude = ["participants", "created_by", "updated_by"]

    def validate(self, data):
        start_date = data.get('start_date')
        start_time = data.get('start_time')
        schedule = data.get('schedule')
        # We validate that the start_date and start_time are not null OR schedule is not empty
        if not start_date and not start_time and not schedule:
            raise serializers.ValidationError('Start date, start time or schedule must be provided')
        if start_date and not start_time:
            raise serializers.ValidationError('Start time must be provided')
        if not start_date and start_time:
            raise serializers.ValidationError('Start date must be provided')
        if start_date and start_time and schedule:
            raise serializers.ValidationError(
                'Start date, start time and schedule cannot be provided at the same time'
            )
        # We validate that we have any participant number or desired participant number
        any_participant_number = data.get('any_participant_number')
        desired_participants_number = data.get('desired_participants_number')
        if not any_participant_number and not desired_participants_number:
            raise serializers.ValidationError('Any participant number or desired participant number must be provided')
        if any_participant_number and desired_participants_number:
            raise serializers.ValidationError(
                'Any participant number and desired participant number cannot be provided at the same time'
            )
        # We validate that we have a free event or a cost
        free = data.get('free')
        cost = data.get('cost')
        if not free and not cost:
            raise serializers.ValidationError('Free or cost must be provided')
        if free and cost:
            raise serializers.ValidationError('Free and cost cannot be provided at the same time')
        # We validate that we have repeatable event with schedule
        repeatable = data.get('repeatable')
        if repeatable and not schedule:
            raise serializers.ValidationError('Repeatable event must have schedule')
        return data

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

        # Create an event chats and add a creator to it
        chat = Chat.objects.create(type=Chat.Type.EVENT)
        chat.participants.add(request.user)
        validated_data["chat_id"] = chat.id

        if validated_data["type"] == "private":
            validated_data["private_token"] = uuid4()

        tags = validated_data.pop("tags", None)
        schedule = validated_data.pop("schedule", None)
        event = Event(**validated_data)
        event.save()
        if schedule:
            for schedule_data in schedule:
                new_schedule = Schedule.objects.create(event=event, **schedule_data)
                event.schedule.add(new_schedule)
        if tags:
            event.tags.set([tag.id for tag in tags])

        return event


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
            instance.private_token = uuid4()
        else:
            instance.private_token = None
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


class EventListSerializer(serializers.ModelSerializer):
    tags = EventTagSerializer(many=True)
    category = EventCategorySerializer(many=False)
    participants_number = serializers.IntegerField()
    average_rating = serializers.FloatField()

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "image_url",
            "description",
            "start_date",
            "end_date",
            "tags",
            "address",
            "category",
            "participants_number",
            "average_rating"
        ]


class EventRetrieveSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)
    tags = EventTagSerializer(many=True)
    category = EventCategorySerializer(many=False)
    created_by = ParticipantSerializer(many=False)
    location = serializers.SerializerMethodField("get_location")
    participants_number = serializers.IntegerField()
    average_rating = serializers.FloatField()

    def get_location(self, obj):
        if not obj.location:
            return None
        return obj.location.coords

    class Meta:
        model = Event
        exclude = ["ratings", "updated_by", "city_south_west_point", "city_north_east_point"]


class EmptySerializer(serializers.Serializer):
    pass
