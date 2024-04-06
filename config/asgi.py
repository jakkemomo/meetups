import os

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.security.websocket import OriginValidator
from django.core.asgi import get_asgi_application

from apps.core.middlewares import JwtAuthMiddlewareStack
from apps.profiles.routers import websocket_urlpatterns
from config.settings import WS_ALLOWED_ORIGINS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'websocket': OriginValidator(
        JwtAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
        allowed_origins=WS_ALLOWED_ORIGINS,
    )
})
