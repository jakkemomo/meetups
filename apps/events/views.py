from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from apps.events.models.events import Event, Categories


class EventCreation(CreateView):
    model = Event
    template_name = 'events/creation.html'
    fields = ['name', 'category', 'address', 'description', 'start_date', 'end_date', 'users']


#
class EventEdition(UpdateView):
    model = Event
    template_name = 'events/etition.html'
    fields = ['name', 'category', 'address', 'description', 'start_date', 'end_date', 'users']


#
#
# class EventDeletion(DeleteView):
#     model = Event
#     template_name = 'events/delition.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['title'] = 'Удаление ивента'
#         return context
#
#
# class EventListing(ListView):
#     model = Event
#     template_name = 'events/events.html'
#     paginate_by = 20
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         category_id = self.kwargs.get('category_id')
#         return queryset.filter(category_id=category_id) if category_id else queryset
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data()
#         context['title'] = 'Доступные ивенты'
#         context['categories'] = Categories.objects.all()
#         return context
#
#
class EventDetail(DetailView):
    model = Event
    template_name = 'events/detail.html'
