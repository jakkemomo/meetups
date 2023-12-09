from django.conf import settings
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import models
from django.db.models import fields
from django.utils import timezone

from apps.core.models import AbstractBaseModel
from apps.events.models.categories import Category
from apps.events.models.rating import Rating
from apps.events.models.tags import Tag

user_model = settings.AUTH_USER_MODEL


class Event(AbstractBaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    tags = models.ManyToManyField(to=Tag, related_name="events", blank=True)
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=True, blank=True, default="Minsk")
    location = PointField(default=Point(27.561831, 53.902284))
    type = fields.CharField(
        max_length=10,
        choices=(("open", "Open"), ("private", "Private")),
        default="open",
        null=False,
        blank=False,
    )
    description = fields.TextField(max_length=250, null=True, blank=True)
    image_url = models.CharField(max_length=250, null=True, blank=True)
    start_date = fields.DateTimeField(null=True, blank=True, default=timezone.now)
    end_date = fields.DateTimeField(null=True, blank=True)

    is_finished = fields.BooleanField(null=False, blank=False, default=False)
    is_visible = fields.BooleanField(null=False, blank=False, default=True)

    participants = models.ManyToManyField(
        user_model, blank=True, related_name="event_participants"
    )
    desired_participants_number = models.PositiveIntegerField(default=1, null=False, blank=False)
    ratings = models.ManyToManyField(user_model, through=Rating, through_fields=("event", "user"))

    class Meta:
        ordering = ["start_date"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name
