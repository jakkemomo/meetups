from .emails import ChangeEmailView, CheckEmailExistsView, ReverifyEmailView, VerifyEmailView
from .passwords import PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from .register import RegisterView
from .tokens import (
    DecoratedTokenBlacklistView,
    DecoratedTokenObtainPairView,
    DecoratedTokenRefreshView,
    DecoratedTokenVerifyView,
)
