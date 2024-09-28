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
    recipient = models.ManyToManyField(user_model, verbose_name="list_of_recipients")
    status = models.CharField(max_length=10, choices=Status.choices, default="PENDING")
    event_url = models.TextField(max_length=250, blank=True)

    class Meta:
        ordering = ["sender"]
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        db_table = "invitations"
