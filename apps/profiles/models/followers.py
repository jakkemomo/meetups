from django.conf import settings
from django.db import models

from apps.core.models import AbstractBaseModel

user_model = settings.AUTH_USER_MODEL


class Follower(AbstractBaseModel):
    class Status(models.TextChoices):
        ACCEPTED = "ACCEPTED"
        PENDING = "PENDING"
        DECLINED = "DECLINED"

    user = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="users")
    follower = models.ForeignKey(user_model, on_delete=models.CASCADE, related_name="followers")
    status = models.CharField(max_length=10, choices=Status.choices, default="PENDING")

    class Meta:
        ordering = ["user"]
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        unique_together = ("user", "follower")
        db_table = "follower"

    def __str__(self):
        return f"{self.follower} following {self.user}"
