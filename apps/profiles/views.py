from django.views.generic import DetailView
from apps.profiles.models.users import User


class ProfileView(DetailView):
    model = User
    template_name = "profiles/profile.html"
