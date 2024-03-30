from django.conf import settings
from django.db import models
from apps.core.models import AbstractBaseModel

user_model = settings.AUTH_USER_MODEL


class Currency(AbstractBaseModel):
    name = models.CharField(max_length=3, unique=True)

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"

    def __str__(self):
        return self.name
