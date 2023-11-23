import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.db.models import Q
from django.views.generic import DetailView
from apps.profiles.models.users import User
from apps.events.models.events import Event
from config import settings


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profiles/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["events"] = (
            Event.objects.filter(Q(is_finished=False) & Q(participants__in=[self.request.user]))
            .order_by("-start_date")
            .values()
        )
        context["old_events"] = (
            Event.objects.filter(Q(is_finished=True) & Q(participants__in=[self.request.user]))
            .order_by("-start_date")
            .values()
        )
        return context

    @staticmethod
    def serialize_user_for_map(context, user_rating):
        geo_user = json.loads(serialize('gejson', user_rating))
        for user in geo_user["features"]:
            attr = user['properties']
            username = attr['username']
            avatar = attr['avatar']
            attr.update(
                {
                    "balloonContent": f'<center><a href="{username}">'
                    + f'<img class="img-responsive" src="{avatar}"'
                    + ' width="50px" height="25x"></a></center>',
                }
            )
        context["user"] = geo_user
        context["yandex_api_key"] = settings.YANDEX_API_KEY
        context["google_api_key"] = settings.GOOGLE_API_KEY
        context["map_provider"] = settings.MAP_PROVIDER
        return context
