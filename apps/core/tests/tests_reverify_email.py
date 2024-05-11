import os
import django
from bs4 import BeautifulSoup
from django.core import mail
from rest_framework import status

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.test.utils import override_settings

from apps.core.tests.models import CoreTestsBase


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class ReverifyEmailTests(CoreTestsBase):
    def setUp(self):
        self.client.post(
            path=self.SIGNUP_PATH,
            data=self.DATA,
            format="json",
        )

    def test_valid(self):
        response = self.client.post(
            path=self.REVERIFY_EMAIL_PATH,
            data={"email": self.DATA.get("email")}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data,"Email successfully sent")

    def test_email_blank(self):
        response = self.client.post(
            path=self.REVERIFY_EMAIL_PATH,
            data={"email": ""},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,"User not found")

    def test_email_invalid(self):
        response = self.client.post(
            path=self.REVERIFY_EMAIL_PATH,
            data={"email": "invalid"},
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data,"User not found")


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class ReverifyEmailTestsAlreadyVerified(CoreTestsBase):
    def setUp(self):
        self.client.post(
            path=self.SIGNUP_PATH,
            data=self.DATA,
            format="json",
        )
        email_data = mail.outbox[0]
        soup = BeautifulSoup(email_data.body, "html.parser")
        email_verification_link = soup.find_all('a')[1].attrs.get("href")
        token = email_verification_link.split("token=")[1]
        self.client.get(self.VERIFY_EMAIL_PATH + f"?token={token}")

    def test_email_verified(self):
        response = self.client.post(
            path=self.REVERIFY_EMAIL_PATH,
            data={"email": self.DATA.get("email")}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data,'Email is already verified')
