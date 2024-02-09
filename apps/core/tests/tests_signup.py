import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework import status
from django.core import mail
from django.test.utils import override_settings

from apps.profiles.models.users import User
from apps.core.tests.models import CoreTestsBase


class SignupTests(CoreTestsBase):

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    )
    def test_valid(self):
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=self.DATA,
            format="json",
        )

        # Testing response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "username": self.DATA.get("username"),
                "email": self.DATA.get("email")
            }
        )

        user = User.objects.filter(email=self.DATA.get("email")).first()

        # Testing user
        self.assertTrue(user)
        self.assertFalse(user.is_email_verified)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

        # Testing emailing
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Activate your account')
        self.assertEqual(mail.outbox[0].to, [user.email])

    # username field
    def test_username_not_provided(self):
        data = {
            "email": "user@example.com",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"username": ["This field is required."]},
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    def test_username_blank(self):
        data = {
            "username": "",
            "email": "user@example.com",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"username": ["This field may not be blank."]},
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    def test_username_short(self):
        data = {
            "username": "1",
            "email": "user@example.com",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "username": ["Ensure this field has at least 2 characters."],
            },
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    def test_username_long(self):
        data = {
            "username": "Village did removed enjoyed explain nor ham saw "
                        "calling talking. Securing as informed declared or "
                        "margaret. Joy horrible moreover man feelings own "
                        "shy. Request norland neither mistake for yet. "
                        "Between the for morning assured country believe. On "
                        "even feet time have an no at. Relation so in "
                        "confined smallest children unpacked delicate. Why "
                        "sir end believe uncivil respect. Always get adieus "
                        "nature day course for common. My little garret "
                        "repair to desire he esteem.",
            "email": "user@example.com",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {
                "username": ["Ensure this field has no more than 128 "
                             "characters."],
            },
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    # email field
    def test_email_not_provided(self):
        data = {
            "username": "test",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"email": ["This field is required."]},
        )

    def test_email_blank(self):
        data = {
            "username": "test",
            "email": "",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,{
                "email": ["This field may not be blank."],
            }
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    def test_email_invalid(self):
        data = {
            "username": "test",
            "email": "invalid@mail",
            "password": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data, format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,{"email": ["Enter a valid email address."]}
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    # password field
    def test_password_not_provided(self):
        data = {
            "email": "user@example.com",
            "username": "test",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"password": ["This field is required."]},
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())

    def test_password_blank(self):
        data = {
            "username": "test",
            "email": "user@example.com",
            "password": "",
        }
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,{
                "password": ["This field may not be blank."],
            }
        )
        self.assertFalse(User.objects.filter(email=data.get("email")).first())


class SignupTestsUserExists(CoreTestsBase):
    def setUp(self):
        self.client.post(path=self.SIGNUP_PATH, data=self.DATA, format="json")

    # email field
    def test_email_exists(self):
        response = self.client.post(
            path=self.SIGNUP_PATH,
            data=self.DATA,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"email": ["This field must be unique."]},
        )
        self.assertTrue(
            User.objects.filter(email=self.DATA.get("email")).first()
        )
