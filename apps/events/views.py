import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    View,
    TemplateView,
)

from apps.events.forms import EventForm
from apps.events.models.events import Event


class EventCreation(CreateView):
    model = Event
    template_name = "events/creation.html"
    form_class = EventForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get_success_url(self):
        if self.object:
            return reverse_lazy("event_detail", kwargs={"pk": self.object.pk})
        else:
            return reverse_lazy("event_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.user.is_authenticated:
                form.instance.created_by = request.user
                form.instance.updated_by = request.user
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EventEdition(UpdateView):
    model = Event
    template_name = "events/edition.html"
    form_class = EventForm

    def get_success_url(self):
        if self.object:
            return reverse_lazy("event_detail", kwargs={"pk": self.object.pk})
        else:
            return reverse_lazy("event_list")


class EventDeletion(DeleteView):
    model = Event
    success_url = reverse_lazy("event_list")


class EventListing(ListView):
    model = Event
    template_name = "events/list.html"
    paginate_by = 20

    def get_queryset(self):
        self.queryset = self.model.objects.filter(Q(is_visible=True) & Q(is_finished=False))
        return super().get_queryset()


class EventDetail(DetailView):
    model = Event
    template_name = "events/detail.html"


class EventMap(TemplateView):
    model = Event
    template_name = "events/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(is_visible=True, is_finished=False)
        geo_events = json.loads(serialize("geojson", events))
        for event in geo_events["features"]:
            attrs = event["properties"]
            event_name = attrs["name"]
            event_start = datetime.strptime(attrs["start_date"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                "%-d %B %H:%M"
            )
            attrs.update(
                {
                    "balloonContentHeader": f"<center>{event_name}</center></br><center>{event_start}</center>",
                    "balloonContent": f'<center><a href="/events/{attrs["pk"]}">'
                    + f'<img class="img-responsive" src="/media/{attrs["image"]}"'
                    + ' width="250px" height="250px"></a></center>',
                    "clusterCaption": f"Событие: {event_name}",
                    "hintContent": event_name,
                }
            )
            event["options"] = {
                "preset": "islands#violetCircleIcon",
                "hideIconOnBalloonOpen": False,
            }
            event["geometry"]["coordinates"].reverse()
        context["events"] = geo_events
        return context


class RegisterToEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.add(request.user)
        return redirect("event_detail", pk=event_id)


class LeaveFromEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.remove(request.user)
        return redirect("event_detail", pk=event_id)


# Finding events within radius
# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import Distance
#
#
# lat = 52.5
# lng = 1.0
# radius = 10
# point = Point(lng, lat)
# Event.objects.filter(location__distance_lt=(point, Distance(km=radius)))
