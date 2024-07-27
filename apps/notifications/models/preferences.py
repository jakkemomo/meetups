from django.db import models

from apps.notifications.models.base import AbstractNotificationsPreferences
from config import settings

user_model = settings.AUTH_USER_MODEL


class EmailNotificationsPreferences(AbstractNotificationsPreferences):
    # System
    system = models.BooleanField(default=True)
    # Events
    event_start = models.BooleanField(default=True)
    new_invite_to_event = models.BooleanField(default=True)
    new_interesting_event_near = models.BooleanField(default=True)
    # Followers events
    new_following_user_event = models.BooleanField(default=True)
    following_user_near_going_to_event = models.BooleanField(default=True)

    class Meta:
        default_related_name = "email_notifications_preferences"


class InAppNotificationsPreferences(AbstractNotificationsPreferences):
    # System
    system = models.BooleanField(default=True)
    # Chat
    new_message = models.BooleanField(default=True)
    # Followers
    new_follower = models.BooleanField(default=True)
    new_follow_request = models.BooleanField(default=True)
    accepted_follow_request = models.BooleanField(default=True)
    # Events
    event_start = models.BooleanField(default=True)
    new_invite_to_event = models.BooleanField(default=True)
    new_interesting_event_near = models.BooleanField(default=True)
    # Followers events
    new_following_user_event = models.BooleanField(default=True)
    following_user_near_going_to_event = models.BooleanField(default=True)

    class Meta:
        default_related_name = "in_app_notifications_preferences"
