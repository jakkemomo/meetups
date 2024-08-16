import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from bs4 import BeautifulSoup
from django.core import mail
from django.test.utils import override_settings
from rest_framework import status

from apps.core.helpers import encode_json_data
from apps.core.tests.models import CoreTestsBase
from apps.profiles.models.users import User


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class VerifyEmailTests(CoreTestsBase):
    def setUp(self):
        self.client.post(path=self.SIGNUP_PATH, data=self.CLIENT_DATA, format="json")

    def test_valid(self):
        # Taking email verification link from email
        email_data = mail.outbox[0]
        soup = BeautifulSoup(email_data.body, "html.parser")
        email_verification_link = soup.find_all("a")[1].attrs.get("href")
        token = email_verification_link.split("token=")[1]

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([*response.data.keys()], ["access"])

    # Testing token
    def test_token_not_provided(self):

        response = self.client.get(self.VERIFY_EMAIL_PATH)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid payload.")

    def test_token_invalid(self):
        token = "invalid"

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid payload.")

    # Testing data
    def test_data_not_provided(self):
        data = {}
        token = encode_json_data(data)

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")

    # Testing user_id
    def test_user_id_not_provided(self):
        data = {"confirmation_token": "token", "email": ''}
        token = encode_json_data(data)

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")

    def test_user_id_invalid(self):
        data = {"user_id": -1, "confirmation_token": "token", "email": ''}
        token = encode_json_data(data)

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.data, "User not found")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Testing confirmation_token
    def test_confirmation_token_not_provided(self):
        user_id = User.objects.filter(email=self.CLIENT_DATA.get("email")).first().id
        data = {"user_id": user_id, "email": ''}
        token = encode_json_data(data)

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")

    def test_confirmation_token_invalid(self):
        User.objects.filter(email=self.CLIENT_DATA.get("email")).first().id

        data = {"confirmation_token": "invalid", "email": ''}
        token = encode_json_data(data)

        response = self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Invalid token.")
