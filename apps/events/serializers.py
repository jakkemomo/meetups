from rest_framework import serializers
from apps.profiles.models import User
from apps.events.models import Event


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "avatar"]


class BaseEventSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField("get_rating")

    def get_rating(self, obj):
        ratings = obj.ratings.through.objects.filter(event=obj).values_list("value", flat=True)
        if not ratings:
            return None
        return sum(ratings) / len(ratings)


class EventListSerializer(BaseEventSerializer):
    class Meta:
        model = Event
        fields = ["name", "rating", "image", "description", "start_date", "end_date"]


class EventRetrieveSerializer(BaseEventSerializer):
    participants = serializers.ListSerializer(child=ParticipantSerializer())

    class Meta:
        model = Event
        exclude = ["ratings"]
