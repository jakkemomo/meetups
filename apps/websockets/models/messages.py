from django.db import models
from django.utils.translation import gettext_lazy as _

from config import settings

user_model = settings.AUTH_USER_MODEL


class Message(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("Created at"),
    )
    created_by = models.ForeignKey(
        to=user_model,
        on_delete=models.CASCADE,
        related_name="messages_created_by",
        verbose_name=_("Created by"),
    )
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
        return f"Message from sender {self.created_by} to chat {self.chat}"
