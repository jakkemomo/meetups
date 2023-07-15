from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from apps.events.forms import EventForm
from apps.events.models.events import Event


class EventCreation(CreateView):
    model = Event
    template_name = "events/creation.html"
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.pk})


class EventEdition(UpdateView):
    model = Event
    template_name = "events/edition.html"
    form_class = EventForm

    def get_success_url(self):
        return reverse_lazy('detail', kwargs={'pk': self.object.pk})


class EventDeletion(DeleteView):
    model = Event
    success_url = reverse_lazy("list")


class EventListing(ListView):
    model = Event
    template_name = 'events/list.html'
    paginate_by = 20

    def get_queryset(self):
        self.queryset = self.model.objects.filter(Q(is_visible=True) & Q(is_finished=False))
        return super().get_queryset()


class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail.html'


class EventMap(ListView):
    model = Event
    template_name = 'events/map.html'
