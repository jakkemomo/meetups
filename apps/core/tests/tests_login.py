import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test.utils import override_settings
from rest_framework import status

from apps.core.tests.models import CoreTestsBase
from apps.profiles.models.users import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class LoginTests(CoreTestsBase):
    def setUp(self):
        self.client.post(path=self.SIGNUP_PATH, data=self.CLIENT_DATA, format="json")

    def test_valid(self):
        data = {"email": "user@example.com", "password": "test"}
        user_record = User.objects.filter(email=data.get("email")).first()
        self.assertIsNotNone(user_record)
        user_record.is_email_verified = True
        user_record.save()

        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([*response.data.keys()], ["refresh", "access"])

    # email field
    def test_email_not_provided(self):
        data = {"username": "test", "password": "test"}
        response = self.client.post(self.LOGIN_PATH, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["This field is required."]})

    def test_email_blank(self):
        data = {"email": "", "password": "test"}
        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"email": ["This field may not be blank."]})

    def test_email_invalid(self):
        data = {"email": "invalid@mail", "password": "test"}
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data, {"detail": "No active account found " "with the given credentials"}
        )

    # password field
    def test_password_not_provided(self):
        data = {"email": "user@example.com"}
        user_record = User.objects.filter(email=data.get("email")).first()
        self.assertTrue(user_record)

        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field is required."]})

    def test_password_blank(self):
        data = {"email": "user@example.com", "password": ""}
        user_record = User.objects.filter(email=data.get("email")).first()
        self.assertTrue(user_record)
        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field may not be blank."]})

    def test_password_invalid(self):
        data = {"email": "user@example.com", "password": "invalid"}
        user_record = User.objects.filter(email=data.get("email")).first()
        user_record.is_email_verified = True

        response = self.client.post(self.LOGIN_PATH, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data, {"detail": "No active account found " "with the given credentials"}
        )
