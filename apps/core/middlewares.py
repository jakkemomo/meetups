import logging

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import UntypedToken

user_model = get_user_model()


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
        except (InvalidToken, TokenError) as e:
            logging.error(e)
            return AnonymousUser()
        token_decoded = token_backend.decode(token_key, verify=False)
        return get_user_model().objects.get(id=token_decoded.get("user_id"))


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
