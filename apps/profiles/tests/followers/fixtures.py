import pytest

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.profiles.models import User
from apps.profiles.models.followers import Follower


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def mock_test_user() -> User:
    return User.objects.create(email="user@example.com", password="test")


@pytest.fixture
def mock_test_user_2() -> User:
    return User.objects.create(email="user2@example.com", password="test2")


@pytest.fixture
def mock_test_user_2_private() -> User:
    return User.objects.create(
        email="user2@example.com",
        password="test2",
        is_private=True,
    )


@pytest.fixture
def mock_follower_accepted(mock_test_user, mock_test_user_2) -> Follower:
    data = {
        'id': 1,
        'user': mock_test_user_2,
        'follower': mock_test_user,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def mock_follower_pending(mock_test_user, mock_test_user_2) -> Follower:
    data = {
        'id': 1,
        'user': mock_test_user_2,
        'follower': mock_test_user,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def mock_follower_declined(mock_test_user, mock_test_user_2) -> Follower:
    data = {
        'id': 1,
        'user': mock_test_user_2,
        'follower': mock_test_user,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)


def get_tokens(user) -> str:
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
