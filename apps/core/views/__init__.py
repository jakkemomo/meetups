from .register import RegisterView
from .emails import (
    VerifyEmailView,
    ReverifyEmailView,
    CheckEmailExistsView,
    ChangeEmailView,
)
from .tokens import (
    DecoratedTokenObtainPairView,
    DecoratedTokenBlacklistView,
    DecoratedTokenVerifyView,
    DecoratedTokenRefreshView,
)
from .passwords import (
    PasswordResetView,
    PasswordResetConfirmView,
    PasswordChangeView,
)
