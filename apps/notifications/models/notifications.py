from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel
from config import settings

user_model = settings.AUTH_USER_MODEL


class Notification(AbstractBaseModel):
    class Status(models.TextChoices):
        NEW = "NEW"
        READ = "READ"

    class Type(models.TextChoices):
        # System
        SYSTEM = "system"
        # Chat
        NEW_MESSAGE = "new_message"
        # Followers
        NEW_FOLLOWER = "new_follower"
        NEW_FOLLOW_REQUEST = "new_follow_request"
        ACCEPTED_FOLLOW_REQUEST = "accepted_follow_request"
        # Events
        EVENT_START = "event_start"
        NEW_INVITE_TO_EVENT = "new_invite_to_event"
        NEW_INTERESTING_EVENT_NEAR = "new_interesting_event_near"
        # Followers events
        NEW_FOLLOWING_USER_EVENT = "new_following_user_event"
        FOLLOWING_USER_NEAR_GOING_TO_EVENT = "following_user_near_going_to_event"

    class Method(models.TextChoices):
        IN_APP = "IN_APP"
        EMAIL = "EMAIL"

    recipient = models.ForeignKey(
        to=user_model,
        on_delete=models.CASCADE,
        related_name="notification_recipient",
        verbose_name=_("Recipient"),
    )
    type = models.CharField(
        max_length=50,
        choices=Type.choices,
        verbose_name=_("Type"),
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default="NEW",
        verbose_name=_("Status"),
    )
    text = models.TextField(
        verbose_name=_("Text"),
        default="New notification"
    )
    additional_data = models.JSONField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Additional data"),
        help_text="Unique data for certain type of notification",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return (
            f"Notification "
            f"from sender {self.created_by if self.created_by else 'System'} "
            f"to {self.recipient}"
        )
