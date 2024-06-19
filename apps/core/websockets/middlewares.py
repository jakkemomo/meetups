import logging

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import UntypedToken

from apps.profiles.models import User

logger = logging.getLogger("core_app")


class JwtAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])
        if b'authorization' in headers:
            token_name, token_key = headers[b'authorization'].decode().split()
            if token_name.lower() == 'bearer':
                scope['user'] = await self.get_user(token_key)
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        try:
            UntypedToken(token_key)
        except (InvalidToken, TokenError) as exc:
            logger.warning(
                f"Invalid JWT token in {self.__class__.__name__}: {exc}"
            )
            return AnonymousUser()
        except Exception as exc:
            logger.exception(exc)
        token_decoded = token_backend.decode(token_key, verify=False)
        return User.objects.get(id=token_decoded.get("user_id"))


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
