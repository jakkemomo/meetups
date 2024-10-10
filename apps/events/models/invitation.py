from django.conf import settings

from django.db import models
from apps.core.models import AbstractBaseModel
from apps.events.models import Event

user_model = settings.AUTH_USER_MODEL


class Invitation(AbstractBaseModel):
    class Status(models.TextChoices):
        ACCEPTED = "ACCEPTED"
        PENDING = "PENDING"
        DECLINED = "DECLINED"

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    sender = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="sender")
    recipient = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="recipient")
    status = models.CharField(max_length=10, choices=Status.choices, default="PENDING")

    class Meta:
        ordering = ["sender"]
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        db_table = "invitations"
        unique_together = ["event", "recipient"]
