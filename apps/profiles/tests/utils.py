from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
