from django.conf import settings
from django.db import models

from apps.core.models import AbstractBaseModel

user_model = settings.AUTH_USER_MODEL


class Review(AbstractBaseModel):
    """Keeps events review by the users.
    Review and Rating are created at the same time.
    Review deleted without Rating. Deleting Rating is cause deleting linked Review."""

    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    review = models.CharField(max_length=1000, null=True)
    rating = models.OneToOneField(
        "events.Rating", related_name="rating", on_delete=models.CASCADE, null=True
    )
    response = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        ordering = ["event"]
        verbose_name = "EventReview"
        verbose_name_plural = "EventReviews"
        unique_together = ("event", "created_by")
        db_table = "events_event_review"
