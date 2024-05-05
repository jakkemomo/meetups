from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel
from config import settings

user_model = settings.AUTH_USER_MODEL


class Notification(AbstractBaseModel):
    class Type(models.TextChoices):
        FOLLOW = "NEW_FOLLOWER"
        FOLLOW_REQUEST = "NEW_FOLLOW_REQUEST"
        ACCEPT = "ACCEPTED_FOLLOW_REQUEST"

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
    additional_data = models.JSONField(
        null=True,
        blank=True,
        default=None,
        verbose_name=_("Additional data"),
        help_text="Unique data for certain type of notification",
    )

    class Meta():
        ordering = ["created_at"]
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

    def __str__(self):
        return (
            f"Notification "
            f"from sender {self.created_by if self.created_by else 'System'} "
            f"to {self.recipient}"
        )
