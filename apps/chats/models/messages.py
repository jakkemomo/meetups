from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import AbstractBaseModel
from config import settings

user_model = settings.AUTH_USER_MODEL


class Message(AbstractBaseModel):
    chat = models.ForeignKey(
        to="Chat",
        on_delete=models.CASCADE,
        related_name="chat_messages",
        verbose_name=_("Chat"),
    )
    message_text = models.TextField(
        max_length=528,
        verbose_name=_("Message text"),
    )

    class Meta():
        ordering = ["created_at"]
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    def __str__(self):
        return f"Message from sender {self.created_by} to chats {self.chat}"
