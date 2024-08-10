from uuid import uuid4

from cities_light.contrib.restframework3 import City
from django.contrib.gis.geos import Point
from django.db import transaction
from rest_framework import serializers

from apps.events.models import Event, Tag, Category, Schedule, Currency
from apps.profiles.models import User
from apps.chats.models import Chat
from . import currency, utils
from .city import LocationSerializer


class ScheduleSerializer(serializers.ModelSerializer):
    day_of_week = serializers.ChoiceField(choices=Schedule.DayOfWeek.choices, required=True)
    time = serializers.TimeField(required=True)

    class Meta:
        model = Schedule
        fields = ["id", "day_of_week", "time"]

class EventCreateSerializer(serializers.ModelSerializer):
    desired_participants_number = serializers.IntegerField(min_value=0, max_value=10000000, default=0, allow_null=True,
                                                           required=False)
    location = LocationSerializer(required=True, many=False)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), required=False, allow_null=True)
    # city_location = city_serializers.CitySerializer()
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
        exclude = ["participants", "created_by", "updated_by", "ratings", "chat"]

    def validate(self, data):
        start_date = data.get('start_date')
        start_time = data.get('start_time')
        schedule = data.get('schedule')
        # We validate that the start_date and start_time are not null OR schedule is not empty
        if not start_date and not start_time and not schedule:
            raise serializers.ValidationError('Start date, start time, or schedule must be provided')
        if start_date and not start_time:
            raise serializers.ValidationError('Start time must be provided')
        if not start_date and start_time:
            raise serializers.ValidationError('Start date must be provided')
        if start_date and start_time and schedule:
            raise serializers.ValidationError(
                'Start date, start time, and schedule cannot be provided at the same time'
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
        currency = data.get('currency')
        if not free and not cost:
            raise serializers.ValidationError('Free or cost must be provided')
        if free and cost:
            raise serializers.ValidationError('Free and cost cannot be provided at the same time')
        if free and currency:
            raise serializers.ValidationError('Free and currency cannot be provided at the same time')
        if cost and not currency or not cost and currency:
            raise serializers.ValidationError('Cost and currency must be provided at the same time')

        # We validate that we have repeatable event with schedule
        repeatable = data.get('repeatable')
        if repeatable and not schedule:
            raise serializers.ValidationError('Repeatable event must have a schedule')
        return data

    @transaction.atomic
    def create(self, validated_data):
        validated_data["location"] = Point(
            (
                validated_data["location"]["longitude"],
                validated_data["location"]["latitude"]
            )
        )
        # city_location = validated_data['city_location']["location"]
        # city = City.objects.filter(
        #     location__within=utils.area_bbox(city_location)
        # ).first()
        # if not city:
        #     city = city_serializers.CitySerializer().create(validated_data['city_location'])
        # validated_data['city_location'] = city
        request = self.context["request"]
        user_id = request.user.id
        validated_data["created_by_id"] = user_id
        validated_data["updated_by_id"] = user_id

        # Create an event chat and add the creator to it
        chat = Chat.objects.create(type=Chat.Type.EVENT)
        chat.participants.add(request.user)
        validated_data["chat_id"] = chat.id

        if validated_data.get("type") == "private":
            validated_data["private_token"] = uuid4()

        tags = validated_data.pop("tags", [])
        schedule = validated_data.pop("schedule", [])

        event = Event(**validated_data)

        if schedule:
            schedule_start = utils.get_schedule_start(schedule)
            event.start_date = schedule_start.date()
            event.start_time = schedule_start.time()
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
    location = LocationSerializer(required=False, many=False)

    def validate(self, data):
        # We validate that we have any participant number or desired participant number
        any_participant_number = data.get('any_participant_number')
        desired_participants_number = data.get('desired_participants_number')
        if any_participant_number and desired_participants_number:
            raise serializers.ValidationError(
                'Any participant number and desired participant number cannot be provided at the same time'
            )

        # We validate that we have a free event or a cost
        free = data.get('free')
        cost = data.get('cost')
        currency = data.get('currency')
        if free and cost:
            raise serializers.ValidationError('Free and cost cannot be provided at the same time')
        if free and currency:
            raise serializers.ValidationError('Free and currency cannot be provided at the same time')
        if 'cost' in data and 'currency' in data and (not cost and currency or cost and not currency):
            raise serializers.ValidationError('Cost and currency must be provided at the same time')
        elif (not cost and not currency) and (
                cost and not self.instance.currency or not self.instance.cost and currency):
            raise serializers.ValidationError('Cost and currency must be provided at the same time')

        # We validate that we have repeatable event with schedule
        repeatable = data.get('repeatable')
        schedule = data.get('schedule')
        if repeatable and not schedule:
            raise serializers.ValidationError('Repeatable event must have a schedule')

        return data

    @transaction.atomic
    def update(self, instance, validated_data):
        location = validated_data.pop("location", None)
        if location:
            instance.location = Point(
                (
                    location.get("longitude"),
                    location.get("latitude")
                )
            )
        # if validated_data.get("city_location"):
        #     utils.update_city_if_exist(instance=instance, validated_data=validated_data)

        schedule_data = validated_data.pop("schedule", None)
        tags = validated_data.pop("tags", None)

        if tags:
            instance.tags.set([tag.id for tag in tags])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if schedule_data:
            schedule_start = utils.get_schedule_start(schedule_data)
            instance.start_date = schedule_start.date()
            instance.start_time = schedule_start.time()

        instance.save()

        if schedule_data:
            self.update_schedules(instance, schedule_data)

        return instance

    def update_schedules(self, instance, schedule_data):
        existing_schedules = instance.schedule.all()
        incoming_schedule_ids = [item.get('id') for item in schedule_data if item.get('id')]

        # Delete schedules not in the incoming data
        for db_schedule in existing_schedules:
            if db_schedule.id not in incoming_schedule_ids:
                db_schedule.delete()

        # Add or update schedules
        for schedule_item in schedule_data:
            schedule_id = schedule_item.get("id")
            if schedule_id:
                # Update existing schedule
                schedule_instance = existing_schedules.filter(id=schedule_id).first()
                if schedule_instance:
                    schedule_instance.day_of_week = schedule_item["day_of_week"]
                    schedule_instance.time = schedule_item["time"]
                    schedule_instance.save()
            else:
                # Add new schedule
                new_schedule = Schedule.objects.create(
                    event=instance,
                    day_of_week=schedule_item["day_of_week"],
                    time=schedule_item["time"],
                )
                instance.schedule.add(new_schedule)


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
    is_favorite = serializers.BooleanField(default=False)

    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "image_url",
            "description",
            "start_date",
            "start_time",
            "end_date",
            "end_time",
            "tags",
            "address",
            "category",
            "participants_number",
            "average_rating",
            "is_favorite",
        ]


class EventRetrieveSerializer(serializers.ModelSerializer):
    tags = EventTagSerializer(many=True)
    category = EventCategorySerializer(many=False)
    created_by = ParticipantSerializer(many=False)
    location = serializers.SerializerMethodField("get_location")
    # city_location = city_serializers.CitySerializer()
    participants_number = serializers.IntegerField()
    average_rating = serializers.FloatField()
    currency = currency.CurrencySerializer(many=False)
    schedule = ScheduleSerializer(many=True)
    is_favorite = serializers.BooleanField(default=False)
    is_participant = serializers.SerializerMethodField("get_is_participant")

    def get_location(self, obj):
        if not obj.location:
            return None
        return obj.location.coords

    def get_is_participant(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        user = request.user
        return obj.participants.filter(id=user.id).exists()

    class Meta:
        model = Event
        exclude = [
            "ratings",
            "updated_by",
            "participants",
        ]


class EmptySerializer(serializers.Serializer):
    pass
