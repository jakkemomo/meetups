from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings


user_model = settings.AUTH_USER_MODEL


class Chat(models.Model):
    class Type(models.TextChoices):
        EVENT = "EVENT"
        DIRECT = "DIRECT"

    type = models.CharField(
        max_length=15,
        choices=Type.choices,
        verbose_name=_("Type"),
    )
    participants = models.ManyToManyField(
        to=user_model,
        blank=True,
        related_name="chat_participants",
        verbose_name=_("Participants"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at"),
    )

    # def clean(self):
    #     super().clean()
        # if not self.id:
        #     return
        #
        # if self.type == self.Type.DIRECT:
        #     max_allowed_participants = 2
        # else:
        #     # TODO: 99 or maximum of event's participants for EVENT type?
        #     max_allowed_participants = 99
        #
        # if self.participants.count() > max_allowed_participants:
        #     raise ValidationError(
        #         f"This chat can have only {max_allowed_participants} "
        #         f"participants"
        #     )

    class Meta():
        ordering = ["created_at"]
        verbose_name = "Chat"
        verbose_name_plural = "Chats"
