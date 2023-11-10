from django.db import models
from django.contrib.auth.models import AbstractUser
from apps.profiles.utils import users_image_upload_path


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    avatar = models.ImageField(
        upload_to=users_image_upload_path,
        null=True,
        blank=True,
        default="users/image/default-user.jpeg",
    )
