import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import override_settings

from apps.profiles.models.users import User
from config.settings import SERVICE_URL


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class LoginTests(APITestCase):
    def setUp(self):
        self.path = f"{SERVICE_URL}api/v1/login/"
        self.client.post(
            path=f"{SERVICE_URL}api/v1/signup/",
            data={
                "username": "test",
                "email": "user@example.com",
                "password": "test",
            },
            format="json",
        )

    def test_valid(self):
        data = {
            "email": "user@example.com",
            "password": "test",
        }
        self.assertTrue(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(self.path, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [*response.data.keys()],
            ["refresh", "access"]
        )

    # email field
    def test_email_not_provided(self):
        data = {
            "username": "test",
            "password": "test",
        }
        response = self.client.post(path=self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"email": ["This field is required."]},
        )

    def test_email_blank(self):
        data = {
            "email": "",
            "password": "test",
        }
        response = self.client.post(path=self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {
                "email": ["This field may not be blank."],
            }
        )

    def test_email_invalid(self):
        data = {
            "email": "invalid@mail",
            "password": "test",
        }
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(path=self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data, {"detail": "No active account found with the given "
                                      "credentials"}
        )

    # password field
    def test_password_not_provided(self):
        data = {
            "email": "user@example.com",
        }
        self.assertTrue(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(path=self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"password": ["This field is required."]},
        )

    def test_password_blank(self):
        data = {
            "email": "user@example.com",
            "password": "",
        }
        self.assertTrue(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(path=self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,{
                "password": ["This field may not be blank."],
            }
        )

    def test_password_invalid(self):
        data = {
            "email": "user@example.com",
            "password": "invalid",
        }
        self.assertTrue(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(self.path, data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data, {"detail": "No active account found with the given "
                                      "credentials"}
        )


