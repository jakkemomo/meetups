from django.db.models import Q
from django.views.generic import DetailView
from apps.profiles.models.users import User
from apps.events.models.events import Event


class ProfileView(DetailView):
    model = User
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = Event.objects.filter(
            Q(is_finished=False) & Q(participants__in=[self.request.user])
        ).order_by('-start_date').values()
        context["old_events"] = Event.objects.filter(
            Q(is_finished=True) & Q(participants__in=[self.request.user])
        ).order_by('-start_date').values()
        return context
