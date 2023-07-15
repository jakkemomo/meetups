from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.events.models.events import Event, Categories


class EventCreation(CreateView):
    model = Event
    template_name = "events/creation.html"
    fields = ["name", "category", "address", "description", "start_date", "end_date", "users"]


class EventEdition(UpdateView):
    model = Event
    template_name = "events/etition.html"
    fields = ["name", "category", "address", "description", "start_date", "end_date", "users"]


class EventDeletion(DeleteView):
    model = Event
    success_url = reverse_lazy("list")


class EventListing(ListView):
    model = Event
    template_name = "events/list.html"
    paginate_by = 20


class EventDetail(DetailView):
    model = Event
    template_name = "events/detail.html"


class EventMap(ListView):
    model = Event
    template_name = "events/map.html"
