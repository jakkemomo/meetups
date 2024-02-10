import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework import status
from django.test.utils import override_settings

from apps.core.tests.models import CoreTestsBase


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class LogoutTests(CoreTestsBase):
    def setUp(self):
        self.client.post(path=self.SIGNUP_PATH, data=self.DATA, format="json")
        response = self.client.post(self.LOGIN_PATH, self.DATA)
        self.refresh_token = response.data.get("refresh")
        self.access_token = response.data.get("access")

    def test_valid(self):
        response = self.client.post(
            self.LOGOUT_PATH, {"refresh": self.refresh_token}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_invalid(self):
        response = self.client.post(self.LOGOUT_PATH, {"refresh": "invalid"})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid",
            }
        )


class LogoutTestsUserLoggedOut(CoreTestsBase):
    def setUp(self):
        self.client.post(path=self.SIGNUP_PATH, data=self.DATA, format="json")
        response = self.client.post(self.LOGIN_PATH, self.DATA)
        self.refresh_token = response.data.get("refresh")
        self.access_token = response.data.get("access")
        self.client.post(self.LOGOUT_PATH, {"refresh": self.refresh_token})

    def test_token_blacklisted(self):
        response = self.client.post(
            self.LOGOUT_PATH, {"refresh": self.refresh_token}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data,
            {
                "detail": "Token is blacklisted",
                "code": "token_not_valid",
            },
        )
