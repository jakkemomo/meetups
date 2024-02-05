import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bs4 import BeautifulSoup

from rest_framework import status
from rest_framework.test import APITestCase
from django.test.utils import override_settings
from django.core import mail

from apps.profiles.models.users import User
from apps.core.helpers import encode_json_data
from config.settings import SERVICE_URL


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class VerifyEmailTests(APITestCase):
    def setUp(self):
        self.path = f"{SERVICE_URL}api/v1/verify/email/"
        self.data = {
                "username": "test",
                "email": "user@example.com",
                "password": "test",
            }
        self.client.post(
            path=f"{SERVICE_URL}api/v1/signup/",
            data=self.data,
            format="json",
        )

    def test_valid(self):
        # Taking email verification link from email
        email_data = mail.outbox[0]
        soup = BeautifulSoup(email_data.body, "html.parser")
        email_verification_link = soup.find_all('a')[1].attrs.get("href")

        self.assertTrue(
            User.objects.filter(email=self.data.get("email")).first()
        )

        response = self.client.get(email_verification_link)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [*response.data.keys()],
            ["access"]
        )

    # Testing token
    def test_token_not_provided(self):
        self.assertTrue(
            User.objects.filter(email=self.data.get("email")).first()
        )

        response = self.client.get(self.path)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid payload.")

    def test_token_invalid(self):
        self.assertTrue(
            User.objects.filter(email=self.data.get("email")).first()
        )
        token = "invalid"

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid payload.")

    # Testing data
    def test_data_not_provided(self):
        data = {}
        token = encode_json_data(data)

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")

    # Testing user_id
    def test_user_id_not_provided(self):
        data = {
            "confirmation_token": "token",
        }
        token = encode_json_data(data)

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")

    def test_user_id_invalid(self):
        data = {
            "user_id": -1,
            "confirmation_token": "token",
        }
        token = encode_json_data(data)

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "User not found")

    # Testing confirmation_token
    def test_confirmation_token_not_provided(self):
        user_id = User.objects.filter(email=self.data.get("email")).first().id
        data = {
            "user_id": user_id,
        }
        token = encode_json_data(data)

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,"Invalid token.")

    def test_confirmation_token_invalid(self):
        user_id = User.objects.filter(email=self.data.get("email")).first().id
        data = {
            "user_id": user_id,
            "confirmation_token": "invalid",
        }
        token = encode_json_data(data)

        response = self.client.get(self.path + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            "Token is invalid or expired. "
            "Please request another confirmation email by signing in."
        )
