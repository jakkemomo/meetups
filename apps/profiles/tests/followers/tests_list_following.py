import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.followers.fixtures import *
from apps.profiles.tests.followers.constants import LIST_FOLLOWING_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_list_following_accepted(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted,
        mock_follower_accepted_reversed,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == mock_test_user.id
    assert response.data[0].get("follower") == mock_test_user_2.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_accepted_private(
        api_client,
        mock_test_user_private,
        mock_test_user_2_private,
        mock_follower_accepted_private,
        mock_follower_accepted_private_reversed,
):
    token = get_tokens(mock_test_user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == mock_test_user_private.id
    assert response.data[0].get("follower") == mock_test_user_2_private.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_pending_private(
        api_client,
        mock_test_user_private,
        mock_test_user_2_private,
        mock_follower_pending_private,
        mock_follower_accepted_private_reversed,
):
    token = get_tokens(mock_test_user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.django_db
def test_list_following_declined_private(
        api_client,
        mock_test_user_private,
        mock_test_user_2_private,
        mock_follower_declined_private,
        mock_follower_accepted_private_reversed,
):
    token = get_tokens(mock_test_user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.django_db
def test_list_following_current_user_accepted(
        api_client,
        mock_test_user,
        mock_test_user_2,
        mock_follower_accepted_reversed,
):
    token = get_tokens(mock_test_user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == mock_test_user.id
    assert response.data[0].get("follower") == mock_test_user_2.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_current_user_pending_private(
        api_client,
        mock_test_user_private,
        mock_test_user_2,
        mock_follower_pending_private_reversed,
):
    token = get_tokens(mock_test_user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_following_current_user_declined_private(
        api_client,
        mock_test_user_private,
        mock_test_user_2,
        mock_follower_declined_private_reversed,
):
    token = get_tokens(mock_test_user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_following_user_not_found(
        api_client,
        mock_test_user,
):
    token = get_tokens(mock_test_user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }


@pytest.mark.django_db
def test_list_following_no_creds(
        api_client,
        mock_test_user,
):
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[mock_test_user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }

