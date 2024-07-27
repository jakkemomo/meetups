import os

import django
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.core.websockets.middlewares import JwtAuthMiddlewareStack
from config.settings import WS_ALLOWED_ORIGINS
from config.urls import websocket_urlpatterns


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': OriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
        allowed_origins=WS_ALLOWED_ORIGINS,
    )
})
