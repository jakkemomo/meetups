from django.db.models import fields
from django.contrib.auth.models import User

from django.db import models

from apps.core.models import BaseModel


class Categories(BaseModel):
    name = fields.CharField(max_length=250)

    def __str__(self):
        return self.name


class Event(BaseModel):
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, related_name="category_events", null=True, blank=True
    )
    name = fields.CharField(max_length=250, unique=True, null=True, blank=True)
    address = fields.CharField(max_length=250, null=True, blank=True)
    description = fields.TextField(max_length=250, null=True, blank=True)
    start_date = fields.DateTimeField(null=True, blank=True)
    end_date = fields.DateTimeField(null=True, blank=True)
    users = models.ManyToManyField(User, null=True, blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/events/{self.id}/"
