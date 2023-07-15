from django.db.models import fields
from django.db import models
from django.conf import settings

from apps.core.models import AbstractBaseModel
from apps.events.utils import events_image_upload_path

user_model = settings.AUTH_USER_MODEL


class Categories(AbstractBaseModel):
    name = fields.CharField(max_length=250)

    def __str__(self):
        return self.name


class Event(AbstractBaseModel):
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=True, blank=True)
    description = fields.TextField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to=events_image_upload_path, null=True, blank=True)

    start_date = fields.DateTimeField(null=True, blank=True)
    end_date = fields.DateTimeField(null=True, blank=True)

    participants = models.ManyToManyField(user_model, blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/events/{self.id}/"
