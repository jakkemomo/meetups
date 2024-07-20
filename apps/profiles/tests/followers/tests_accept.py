import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.utils import get_tokens
from apps.profiles.tests.followers.constants import ACCEPT_URL
from apps.profiles.models.followers import Follower


@pytest.mark.usefixtures(
    "follower_user_pending_private",
)
@pytest.mark.django_db
def test_accept_pending_private(
        api_client,
        user_private,
        user_2_private,
):
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user_private.id])
    )
    assert response.status_code == 200
    assert response.data.get('user')["id"] == user_2_private.id
    assert response.data.get('follower')["id"] == user_private.id
    assert response.data.get('status') == Follower.Status.ACCEPTED


@pytest.mark.usefixtures(
    "follower_user_declined_private",
)
@pytest.mark.django_db
def test_accept_declined_private(
        api_client,
        user_private,
        user_2_private,
):
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user_private.id])
    )
    assert response.status_code == 200
    assert response.data.get('user')["id"] == user_2_private.id
    assert response.data.get('follower')["id"] == user_private.id
    assert response.data.get('status') == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_accept_current_user(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_accept_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }


@pytest.mark.django_db
def test_accept_no_creds(
        api_client,
        user,
):
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }


@pytest.mark.usefixtures(
    "follower_user_accepted",
)
@pytest.mark.django_db
def test_accept_accepted(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user.id])
    )
    assert response.status_code == 409
    assert response.data == {
        'detail': f'{user} is already following you',
    }


@pytest.mark.django_db
def test_accept_follower_not_found(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[user.id])
    )
    assert response.status_code == 404
    assert response.data == {'detail': 'No such follow requests was found'}
