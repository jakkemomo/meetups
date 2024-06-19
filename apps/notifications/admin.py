from django.contrib import admin
from .models import Notification
from .models.preferences import (
    InAppNotificationsPreferences,
    EmailNotificationsPreferences,
)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'recipient', 'type', 'created_at')
    list_filter = ('type', 'created_at')
    search_fields = ('id', 'created_by__username', 'recipient__username')
    readonly_fields = ('created_at',)


@admin.register(EmailNotificationsPreferences)
class EmailNotificationsPreferencesAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "system",
        "event_start",
        "new_invite_to_event",
        "new_interesting_event_near",
        "new_following_user_event",
        "following_user_near_going_to_event",
    )
    search_fields = ("user__username", "user__email")
    list_filter = (
        "user",
        "system",
        "event_start",
        "new_invite_to_event",
        "new_interesting_event_near",
        "new_following_user_event",
        "following_user_near_going_to_event",
    )


@admin.register(InAppNotificationsPreferences)
class InAppNotificationsPreferencesAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "system",
        "event_start",
        "new_invite_to_event",
        "new_interesting_event_near",
        "new_following_user_event",
        "following_user_near_going_to_event",
        "new_message",
        "new_follower",
        "new_follow_request",
        "accepted_follow_request",
    )
    search_fields = ("user__username", "user__email")
    list_filter = (
        "user",
        "system",
        "event_start",
        "new_invite_to_event",
        "new_interesting_event_near",
        "new_following_user_event",
        "following_user_near_going_to_event",
        "new_message",
        "new_follower",
        "new_follow_request",
        "accepted_follow_request",
    )
