from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    class Gender(models.TextChoices):
        MALE = "MALE"
        FEMALE = "FEMALE"
        NONE = "NONE"

    class Type(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL"
        COMPANY = "COMPANY"

    username = models.CharField(max_length=128, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    city = models.ForeignKey("cities_light.City", on_delete=models.PROTECT, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    bio = models.CharField(max_length=1000, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=15, choices=Gender.choices, verbose_name=_("Gender"), default=Gender.NONE
    )
    type = models.CharField(
        max_length=15, choices=Type.choices, verbose_name=_("Type"), default=Type.INDIVIDUAL
    )
    is_private = models.BooleanField(
        verbose_name="Profile private status",
        default=False,
        help_text="Designates is user profile is private.",
    )
    category_favorite = models.ManyToManyField(
        to="events.Category", db_table="user_category_favorite", related_name="categories_favorite"
    )
    # These fields are using in AbstractUser model
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
