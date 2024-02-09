from django.db import models
from django.contrib.auth.models import AbstractUser

from apps.profiles.models.city import City


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    username = models.CharField(max_length=128, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_DEFAULT, default=1)
    is_email_verified = models.BooleanField(default=False)

    # These fields are using in AbstractUser model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]
