from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View
from apps.events.models.events import Event, Categories
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class EventCreation(CreateView):
    model = Event
    template_name = 'events/creation.html'
    fields = ['name', 'category', 'address', 'description', 'start_date', 'end_date', 'participants']


class EventEdition(UpdateView):
    model = Event
    template_name = 'events/edition.html'
    fields = ['name', 'category', 'address', 'description', 'start_date', 'end_date', 'participants']


class EventDeletion(DeleteView):
    model = Event
    success_url = reverse_lazy("list")


class EventListing(ListView):
    model = Event
    template_name = 'events/list.html'
    paginate_by = 20


class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail.html'


class EventMap(ListView):
    model = Event
    template_name = 'events/map.html'


class RegisterToEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.add(request.user)
        return redirect('event_detail', pk=event_id)


class LeaveFromEvent(LoginRequiredMixin, View):
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        event.participants.remove(request.user)
        return redirect('event_detail', pk=event_id)
