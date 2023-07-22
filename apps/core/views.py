from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic


class CoreSignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("core:login")
    template_name = "registration/signup.html"


class CoreLoginView(LoginView):
    next = reverse_lazy("events:event_map")

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")


class CoreLogoutView(LogoutView):
    next = reverse_lazy("events:event_map")

    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")
