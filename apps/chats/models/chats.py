from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel
from config import settings

user_model = settings.AUTH_USER_MODEL


class Chat(AbstractBaseModel):
    class Type(models.TextChoices):
        EVENT = "EVENT"
        DIRECT = "DIRECT"

    type = models.CharField(max_length=15, choices=Type.choices, verbose_name=_("Type"))
    participants = models.ManyToManyField(
        to=user_model, blank=True, related_name="chat_participants", verbose_name=_("Participants")
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
