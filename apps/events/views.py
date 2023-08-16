import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.postgres.search import TrigramWordSimilarity
from django.core.serializers import serialize
from django.db.models import Q
from django.db.models.functions import Greatest
from django.shortcuts import get_object_or_404, redirect, render
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
from apps.events.models.categories import Category
from apps.events.models.rating import Rating
from config import settings


class EventCreation(LoginRequiredMixin, CreateView):
    model = Event
    template_name = "events/creation.html"
    form_class = EventForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def get_success_url(self):
        if self.object:
            return reverse_lazy("events:event_detail", kwargs={"pk": self.object.pk})
        else:
            return reverse_lazy("events:event_list")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            if request.user.is_authenticated:
                form.instance.created_by = request.user
                form.instance.updated_by = request.user
            if form.instance.type == "private":
                form.instance.is_visible = False
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EventEdition(LoginRequiredMixin, UpdateView):
    model = Event
    template_name = "events/edition.html"
    form_class = EventForm

    def get_success_url(self):
        if self.object:
            return reverse_lazy("events:event_detail", kwargs={"pk": self.object.pk})
        else:
            return reverse_lazy("events:event_list")

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            if form.instance.type == "private":
                form.instance.is_visible = False
            else:
                form.instance.is_visible = True
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EventDeletion(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy("events:event_list")


class EventListing(ListView):
    model = Event
    template_name = "events/list.html"
    paginate_by = 20

    def get_queryset(self):
        if self.request.user.id:
            self.queryset = self.model.objects.filter(
                Q(is_visible=True) & Q(is_finished=False)
                | Q(participants__in=[self.request.user]) & Q(is_finished=False)
            ).distinct()
        else:
            self.queryset = self.model.objects.filter(Q(is_visible=True) & Q(is_finished=False))
        return super().get_queryset()

    def post(self, request):
        search_request = request.POST["searched"]
        category = request.POST["category"]

        object_list = Event.objects.annotate(
            similarity=Greatest(
                TrigramWordSimilarity(search_request, "name"),
                TrigramWordSimilarity(search_request, "description"),
                TrigramWordSimilarity(search_request, "address"),
            )
        ).filter(similarity__gt=0.5).order_by("-similarity") if search_request else self.get_queryset()

        if category:
            object_list = object_list.filter(category__name=category)

        context = self.get_context_data(object_list=object_list if object_list else self.get_queryset())
        context.update({"searched": search_request, "object_list": object_list, "category": category})

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class EventDetail(DetailView):
    model = Event
    template_name = "events/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rating_object = Rating.objects.filter(
            event=self.object, user=self.request.user if self.request.user.id else None
        ).first()
        context["rating_object"] = rating_object
        EventMap.serialize_events_for_map(context, [self.object])
        return context


class EventMap(TemplateView):
    model = Event
    template_name = "events/map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(is_visible=True, is_finished=False)
        self.serialize_events_for_map(context, events)
        return context

    @staticmethod
    def serialize_events_for_map(context, events):
        geo_events = json.loads(serialize("geojson", events))
        for event in geo_events["features"]:
            attrs = event["properties"]
            event_name = attrs["name"]
            event_start = datetime.strptime(attrs["start_date"], "%Y-%m-%dT%H:%M:%SZ").strftime(
                "%-d %B %H:%M"
            )
            attrs["start_date"] = event_start
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
        context["yandex_api_key"] = settings.YANDEX_API_KEY
        context["google_api_key"] = settings.GOOGLE_API_KEY
        context["map_provider"] = settings.MAP_PROVIDER
        return context


class RegisterToEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.add(request.user)
        event.current_participants_number += 1
        event.save()
        return redirect("events:event_detail", pk=event_id)


class LeaveFromEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.remove(request.user)
        event.current_participants_number -= 1
        event.save()
        return redirect("events:event_detail", pk=event_id)


class RateEvent(LoginRequiredMixin, View):
    model = Rating

    def post(self, request, event_id, value=None):
        event = get_object_or_404(Event, id=event_id)
        rating_object, created = Rating.objects.get_or_create(event=event, user=request.user)

        if value:
            rating_object.value = value
            rating_object.save()
        else:
            rating_object.delete()

        return redirect("events:event_detail", pk=event_id)


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
