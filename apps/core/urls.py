from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)

from .views import CoreSignUpView, CoreLoginView, CoreLogoutView

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
    path("signup/", CoreSignUpView.as_view(), name="signup"),
    path("login/", CoreLoginView.as_view(), name="login"),
    path("logout/", CoreLogoutView.as_view(), name="logout"),
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/v1/login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/logout/", TokenBlacklistView.as_view(), name="api_logout"),
]
