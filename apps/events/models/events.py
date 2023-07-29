from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import models
from django.db.models import fields
from django.utils import timezone
from location_field.models.spatial import LocationField

from apps.core.models import AbstractBaseModel
from apps.events.models.categories import Category
from apps.events.models.rating import Rating
from apps.events.models.tags import Tag
from apps.events.utils import events_image_upload_path
from common.mixins import ResizeImageMixin

user_model = settings.AUTH_USER_MODEL


class Event(AbstractBaseModel, ResizeImageMixin):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="events", blank=True)
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=True, blank=True)
    description = fields.TextField(max_length=250, null=True, blank=True)
    image = models.ImageField(
        upload_to=events_image_upload_path,
        null=True,
        blank=True,
        default="events/image/default-event.jpg",
    )
    start_date = fields.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = fields.DateTimeField(null=True, blank=True)

    is_finished = fields.BooleanField(null=False, blank=False, default=False)
    is_visible = fields.BooleanField(null=False, blank=False, default=True)

    participants = models.ManyToManyField(user_model, blank=True, related_name='event_participants')
    ratings = models.ManyToManyField(user_model, through=Rating, through_fields=("event", "user"))

    place = models.CharField(max_length=255, default="Minsk")
    location = LocationField(based_fields=["place"], zoom=13, default=Point(27.561831, 53.902284))

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/events/{self.id}/"

    def save(self, *args, **kwargs):
        if self.pk is None or Event.objects.get(pk=self.pk).image != self.image:
            self.resize(self.image, (400, 500))
        super().save(*args, **kwargs)
