from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    username = models.CharField(max_length=128, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    #bio = models.CharField(max_length=1000, null=True, blank=True)
    #age = models.PositiveIntegerField(default=18, validators=[MinValueValidator(1), MaxValueValidator(100)])

    # These fields are using in AbstractUser model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", ]
