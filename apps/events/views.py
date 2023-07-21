from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView, View

from apps.events.forms import EventForm
from apps.events.models.events import Event, Categories


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

    def post(self, request):
        searched = request.POST["searched"]
        category = request.POST["category"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        self.object_list = self.get_queryset()

        object_list = Event.objects.filter(
            (Q(name__icontains=searched) |
             Q(address__icontains=searched) |
             Q(description__icontains=searched) |
             Q(category__name__icontains=searched))
        )

        if category:
            object_list = object_list.filter(category__name=category)
        if start_date:
            object_list = object_list.filter(start_date__gte=start_date)
        if end_date:
            object_list = object_list.filter(end_date__lte=end_date)

        context = self.get_context_data()
        context.update({
            "searched": searched,
            "object_list": object_list,
            "category": category,
            "start_date": start_date,
            "end_date": end_date
        })

        return render(request, self.template_name, context)

    def get_context_data(self):
        context = super().get_context_data()
        context["categories"] = Categories.objects.all()
        return context


class EventDetail(DetailView):
    model = Event
    template_name = "events/detail.html"


class EventMap(ListView):
    model = Event
    template_name = "events/map.html"


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
