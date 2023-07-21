from django import forms
from django.forms import SelectDateWidget

from apps.events.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["name", "image", "category", "tags", "address", "description", "start_date", "end_date", "participants",
                  "is_visible", "is_finished"]
        widgets = {
            'start_date': SelectDateWidget(),
            'end_date': SelectDateWidget()
        }
