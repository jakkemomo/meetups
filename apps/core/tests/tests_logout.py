import os
import django
from django.urls import reverse

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import override_settings


class LogoutTestsBase(APITestCase):
    SIGNUP_PATH = reverse('core:signup')
    LOGIN_PATH = reverse('core:login')
    LOGOUT_PATH = reverse('core:logout')
    DATA = {
            "username": "test",
            "email": "user@example.com",
            "password": "test",
        }


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class LogoutTests(LogoutTestsBase):
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


class LogoutTestsUserLoggedOut(LogoutTestsBase):
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
