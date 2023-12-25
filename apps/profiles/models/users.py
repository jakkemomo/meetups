from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    image_url = models.CharField(max_length=250, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
