from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

user_model = settings.AUTH_USER_MODEL


class AbstractBaseModel(models.Model):
    created_by = models.ForeignKey(
        to=user_model,
        verbose_name=_("Created by"),
        null=True,
        blank=True,
        related_name="%(class)s_created",
        on_delete=models.SET_NULL,
    )

    created_at = models.DateTimeField(
        verbose_name=_("Created at"), auto_now_add=True, editable=False,
    )

    updated_by = models.ForeignKey(
        to=user_model,
        verbose_name=_("Updated by"),
        null=True,
        blank=True,
        related_name="%(class)s_updated",
        on_delete=models.SET_NULL,
    )

    updated_at = models.DateTimeField(
        verbose_name=_("Updated at"), auto_now=True, null=True, blank=True
    )

    class Meta:
        abstract = True
