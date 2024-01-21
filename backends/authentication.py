from django.contrib.auth.backends import BaseBackend

from apps.profiles.models import User


class AuthenticationWithoutPassword(BaseBackend):
    def authenticate(self, request, **kwargs):
        email = kwargs.get("email", "")
        if not email:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.is_email_verified:
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
