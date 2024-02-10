from django.db import models
from apps.core.models import AbstractBaseModel
from django.conf import settings

user_model = settings.AUTH_USER_MODEL


class Review(AbstractBaseModel):
    """Keeps events review by the users"""
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, db_index=True)
    review = models.CharField(max_length=1000, null=True)
    created_by = None
    updated_by = None

    class Meta:
        ordering = ['event']
        verbose_name = "EventReview"
        verbose_name_plural = "EventReviews"
        unique_together = ("event", "user")
        db_table = 'events_event_review'
