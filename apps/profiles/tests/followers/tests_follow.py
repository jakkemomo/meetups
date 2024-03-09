import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.followers.fixtures import (
    api_client,
    mock_test_user,
    mock_test_user_2,
    mock_test_user_2_private,
    mock_follower_accepted,
    mock_follower_pending,
    mock_follower_declined,
    get_tokens,
)
from apps.profiles.tests.followers.constants import FOLLOW_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_follow_valid(
        api_client,
        mock_test_user,
        mock_test_user_2,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 201
    assert response.data['id'] is not None
    assert response.data['user'] == mock_test_user_2.id
    assert response.data['follower'] == mock_test_user.id
    assert response.data['status'] == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_follow_private_valid(
        api_client,
        mock_test_user,
        mock_test_user_2_private,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 201
    assert response.data['id'] is not None
    assert response.data['user'] == mock_test_user_2_private.id
    assert response.data['follower'] == mock_test_user.id
    assert response.data['status'] == Follower.Status.PENDING


@pytest.mark.django_db
def test_follow_current_user(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_follow_user_not_found(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }


@pytest.mark.django_db
def test_follow_no_creds(
        api_client,
        mock_test_user,
):
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }


@pytest.mark.django_db
def test_follow_accepted(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Already following'}


@pytest.mark.django_db
def test_follow_pending(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_pending,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Follow request already sent'}


@pytest.mark.django_db
def test_follow_declined(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_declined,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Follow request already sent'}
