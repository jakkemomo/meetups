app_name = "core"

from django.urls import path

from .views import CoreSignUpView, CoreLoginView, CoreLogoutView


urlpatterns = [
    path("signup/", CoreSignUpView.as_view(), name="signup"),
    path("login/", CoreLoginView.as_view(), name="login"),
    path("logout/", CoreLogoutView.as_view(), name="logout"),
]
