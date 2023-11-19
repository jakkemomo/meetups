from django import forms
from django.forms import DateTimeInput

from apps.events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "name",
            "image_url",
            "type",
            "category",
            "tags",
            "address",
            "location",
            "desired_participants_number",
            "description",
            "participants",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": DateTimeInput(
                format=("%Y-%m-%dT%H:%M"), attrs={"type": "datetime-local"}
            ),
            "end_date": DateTimeInput(format=("%Y-%m-%dT%H:%M"), attrs={"type": "datetime-local"}),
            "tags": forms.CheckboxSelectMultiple,
        }
