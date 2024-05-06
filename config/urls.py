"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from apps.chats.consumers import ChatConsumer
from apps.notifications.consumers import NotificationConsumer

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls", namespace="core")),
    path("", include('apps.upload.urls', namespace="upload")),
    path("", include("apps.events.urls", namespace="events")),
    path("", include("apps.profiles.urls", namespace="profiles")),
    path("", include("apps.chats.urls", namespace="chats")),
    path("", include("apps.notifications.urls", namespace="notifications")),
    path("__debug__/", include("debug_toolbar.urls")),

]

websocket_urlpatterns = [
    re_path(r"ws/notifications/", NotificationConsumer.as_asgi()),
    re_path(r"ws/chats/(?P<chat_id>[^/.]+)", ChatConsumer.as_asgi()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
