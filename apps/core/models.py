from cities_light.abstract_models import (
    AbstractCity,
    AbstractRegion,
    AbstractCountry,
    AbstractSubRegion,
)
from cities_light.receivers import connect_default_signals
from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.contrib.postgres.indexes import GinIndex
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
        verbose_name=_("Created at"), auto_now_add=True, editable=False
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


class Country(AbstractCountry):
    pass


connect_default_signals(Country)


class Region(AbstractRegion):
    pass


connect_default_signals(Region)


class SubRegion(AbstractSubRegion):
    pass


connect_default_signals(SubRegion)


class City(AbstractCity):
    point = PointField(null=True)

    def save(self, *args, **kwargs):
        if not self.point:
            self.point = Point(float(self.longitude), float(self.latitude))

        self.latitude = self.point.y
        self.longitude = self.point.x
        super().save(*args, **kwargs)

    class Meta:
        indexes = [
            GinIndex(
                name="trigram_city_name_ru_idx", fields=["name_ru"], opclasses=["gin_trgm_ops"]
            ),
            GinIndex(
                name="trigram_city_name_en_idx", fields=["name_en"], opclasses=["gin_trgm_ops"]
            ),
        ]


connect_default_signals(City)
