from django.conf import settings
from django.db import models
from apps.core.models import AbstractBaseModel
from apps.profiles.models import User

user_model = settings.AUTH_USER_MODEL


class UserRating(AbstractBaseModel):
    """Keeps rating for a user with comments"""
    value = models.SmallIntegerField(null=True, default=0)
    user_rater = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rater")
    user_rated = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rated")
    comment = models.CharField(max_length=256, null=True)

    class Meta:
        ordering = ["-value"]
        verbose_name = "UserRating"
        verbose_name_plural = "UserRatings"
        db_table = 'user_rating'

    def __str__(self):
        return f'{self.user_rater} rated {self.user_rated} as {self.value} with comment {self.comment}'
