from django.conf import settings
from django.db import models
from apps.core.models import AbstractBaseModel

user_model = settings.AUTH_USER_MODEL


class Rating(AbstractBaseModel):
    value = models.SmallIntegerField(null=True)
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)

    class Meta:
        ordering = ["value"]
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ("event", "user")

    def __str__(self):
        return f"{self.user} rated {self.event} with {self.value}"
