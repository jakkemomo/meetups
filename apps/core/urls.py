from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    DecoratedTokenObtainPairView,
    DecoratedTokenBlacklistView,
    DecoratedTokenVerifyView,
    DecoratedTokenRefreshView,
    RegisterView,
    VerifyEmailView,
    ReverifyEmailView,
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordResetChangeView,
    PasswordChangeView,
)

app_name = "core"

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/signup/", RegisterView.as_view(), name="signup"),
    path("api/v1/login/", DecoratedTokenObtainPairView.as_view(), name="login"),
    path("api/v1/logout/", DecoratedTokenBlacklistView.as_view(), name="logout"),
    path("api/v1/verify/email/", VerifyEmailView.as_view(), name="verify-email"),
    path("api/v1/reverify/email/", ReverifyEmailView.as_view(), name="reverify-email"),
    path("api/v1/token/refresh/", DecoratedTokenRefreshView.as_view(), name="token-refresh"),
    path("api/v1/token/verify/", DecoratedTokenVerifyView.as_view(), name="token-verify"),
    path("api/v1/password/reset/", PasswordResetView.as_view(), name="password-reset"),
    path("api/v1/password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("api/v1/password/reset/change/", PasswordResetChangeView.as_view(), name="password-reset-change"),
    path("api/v1/password/change/", PasswordChangeView.as_view(), name="password-change"),
]
