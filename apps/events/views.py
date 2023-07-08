from django.views.generic import CreateView, ListView, DetailView
from apps.events.models.events import Event, Categories


class EventCreation(CreateView):
    model = Event
    template_name = 'events/creation.html'
    fields = ['name', 'category', 'address', 'description', 'start_date', 'end_date', 'users']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventCreation, self).get_context_data()
        context['title'] = 'Создание ивента'
        return context


class EventListing(ListView):
    model = Event
    template_name = 'events/events.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super(EventListing, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventListing, self).get_context_data()
        context['title'] = 'Доступные ивенты'
        context['categories'] = Categories.objects.all()
        return context


class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail.html'

    def get_object(self, queryset=None):
        category_id = self.kwargs.get('category_id')
        event_id = self.kwargs.get('event_id')
        return Event.objects.get(category_id=category_id, id=event_id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EventDetail, self).get_context_data()
        event = self.get_object()
        context['title'] = f'Ивент {event.name}'
        return context
