from django.conf import settings
from django.db import models

user_model = settings.AUTH_USER_MODEL


class FavoriteEvent(models.Model):
    """Keeps events favorite by the user"""
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE, db_index=True)

    class Meta:
        ordering = ['user']
        verbose_name = "FavoriteEvent"
        verbose_name_plural = "FavoriteEvents"
        unique_together = ("event", "user")
        db_table = 'events_favorite'
