from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import login as auth_login, get_user_model
from django.conf import settings


User = get_user_model()


class CoreSignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("events:event_map")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        result = super(CoreSignUpView, self).form_valid(form)
        auth_login(self.request, self.object)
        return result


class CoreLoginView(LoginView):
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")


class CoreLogoutView(LogoutView):
    def get_success_url(self):
        url = self.get_redirect_url()
        if url:
            return url
        else:
            return reverse_lazy("events:event_map")
