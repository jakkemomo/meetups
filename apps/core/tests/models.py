from django.urls import reverse
from rest_framework.test import APITestCase


class CoreTestsBase(APITestCase):
    SIGNUP_PATH = reverse("core:signup")
    LOGIN_PATH = reverse("core:login")
    LOGOUT_PATH = reverse("core:logout")
    VERIFY_EMAIL_PATH = reverse("core:verify-email")
    REVERIFY_EMAIL_PATH = reverse("core:reverify-email")
    CLIENT_DATA = {"username": "test", "email": "user@example.com", "password": "test"}
