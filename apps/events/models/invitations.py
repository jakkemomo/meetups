from django.db import models
from apps.core.models import AbstractBaseModel


class Invitation(AbstractBaseModel):
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    sender = models.ForeignKey(
        "profiles.User", related_name="sent_invitations", on_delete=models.CASCADE
    )
    recipient = models.ForeignKey(
        "profiles.User", related_name="received_invitations", on_delete=models.CASCADE
    )
    accepted = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
