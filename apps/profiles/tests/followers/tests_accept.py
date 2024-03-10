import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.followers.fixtures import *
from apps.profiles.tests.followers.constants import ACCEPT_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_accept_pending_private(
        api_client,
        mock_test_user,
        mock_test_user_2_private,
        mock_follower_pending_private,
):
    token = get_tokens(mock_test_user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 200
    assert response.data.get('id') is not None
    assert response.data.get('user') == mock_test_user_2_private.id
    assert response.data.get('follower') == mock_test_user.id
    assert response.data.get('status') == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_accept_declined_private(
        api_client,
        mock_test_user,
        mock_test_user_2_private,
        mock_follower_declined_private,
):
    token = get_tokens(mock_test_user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 200
    assert response.data.get('id') is not None
    assert response.data.get('user') == mock_test_user_2_private.id
    assert response.data.get('follower') == mock_test_user.id
    assert response.data.get('status') == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_accept_current_user(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_accept_user_not_found(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
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
        mock_test_user,
):
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }


@pytest.mark.django_db
def test_accept_accepted(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted,
):
    token = get_tokens(mock_test_user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 409
    assert response.data == {
        'detail': f'{mock_test_user} is already following you',
    }


@pytest.mark.django_db
def test_accept_follower_not_found(
        api_client,
        mock_test_user,
        mock_test_user_2,
):
    token = get_tokens(mock_test_user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(ACCEPT_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 404
    assert response.data == {'detail': 'No such follow requests was found'}
