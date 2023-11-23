from django.conf import settings
from django.db import models
from apps.core.models import AbstractBaseModel


user_model = settings.AUTH_USER_MODEL


class UserActivityRating(AbstractBaseModel):
    value = models.SmallIntegerField(null=True)
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-value"]
        verbose_name = "UserRating"
        verbose_name_plural = "UserRatings"
        db_table = 'user_activity_rating'

    def __str__(self):
        return f'{self.user} activity rated as {self.value}'
