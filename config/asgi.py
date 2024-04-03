from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter

from django.core.asgi import get_asgi_application

from apps.core.middlewares import JwtAuthMiddlewareStack

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')


from apps.profiles.routers import websocket_urlpatterns


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': JwtAuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    )
})