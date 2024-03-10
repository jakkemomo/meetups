import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.followers.fixtures import *
from apps.profiles.tests.followers.constants import UNFOLLOW_URL


@pytest.mark.django_db
def test_unfollow_accepted_valid(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You are no longer following {mock_test_user_2}'
    }


@pytest.mark.django_db
def test_unfollow_pending_valid_private(
        api_client,
        mock_test_user,
        mock_test_user_2_private,
        mock_follower_pending_private,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You canceled follow request to {mock_test_user_2_private}'
    }


@pytest.mark.django_db
def test_unfollow_declined_valid_private(
        api_client,
        mock_test_user,
        mock_test_user_2_private,
        mock_follower_declined_private,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You canceled follow request to {mock_test_user_2_private}'
    }


@pytest.mark.django_db
def test_unfollow_current_user(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_unfollow_user_not_found(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }


@pytest.mark.django_db
def test_unfollow_no_creds(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted,
):
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }


@pytest.mark.django_db
def test_unfollow_follower_not_found(
        api_client,
        mock_test_user,
        mock_test_user_2,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': f'You are not following {mock_test_user_2}'
    }
