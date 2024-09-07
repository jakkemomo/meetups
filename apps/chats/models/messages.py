from django.contrib.postgres.indexes import GinIndex
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel
from config import settings

user_model = settings.AUTH_USER_MODEL


class Message(AbstractBaseModel):
    class Status(models.TextChoices):
        UNREAD = "unread"
        READ = "read"
        DELETED = "deleted"

    chat = models.ForeignKey(
        to="Chat", on_delete=models.CASCADE, related_name="chat_messages", verbose_name=_("Chat")
    )
    message_text = models.TextField(max_length=528, verbose_name=_("Message text"))
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.UNREAD, verbose_name=_("Status")
    )
    read_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Read at"))

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        indexes = [
            GinIndex(name="trigram_text_idx", fields=["message_text"], opclasses=["gin_trgm_ops"])
        ]

    def __str__(self):
        return f"Message from sender {self.created_by} to chats {self.chat}"
