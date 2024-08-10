from rest_framework import serializers

from apps.notifications.models import EmailNotificationsPreferences, InAppNotificationsPreferences


class EmailNotificationsPreferencesRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotificationsPreferences
        fields = [
            "user",
            "system",
            "event_start",
            "new_invite_to_event",
            "new_interesting_event_near",
            "new_following_user_event",
            "following_user_near_going_to_event",
        ]


class EmailNotificationsPreferencesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailNotificationsPreferences
        fields = [
            "system",
            "event_start",
            "new_invite_to_event",
            "new_interesting_event_near",
            "new_following_user_event",
            "following_user_near_going_to_event",
        ]


class InAppNotificationsPreferencesRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotificationsPreferences
        fields = [
            "user",
            "system",
            "new_message",
            "new_follower",
            "new_follow_request",
            "accepted_follow_request",
            "event_start",
            "new_invite_to_event",
            "new_interesting_event_near",
            "new_following_user_event",
            "following_user_near_going_to_event",
        ]


class InAppNotificationsPreferencesUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = InAppNotificationsPreferences
        fields = [
            "system",
            "new_message",
            "new_follower",
            "new_follow_request",
            "accepted_follow_request",
            "event_start",
            "new_invite_to_event",
            "new_interesting_event_near",
            "new_following_user_event",
            "following_user_near_going_to_event",
        ]
