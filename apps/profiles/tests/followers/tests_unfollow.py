import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.fixtures import *
from apps.profiles.tests.followers.constants import UNFOLLOW_URL


@pytest.mark.django_db
def test_unfollow_accepted_valid(
        api_client,
        user,
        user_2,
        follower_user_accepted,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You are no longer following {user_2}'
    }


@pytest.mark.django_db
def test_unfollow_pending_valid_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_pending_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You canceled follow request to {user_2_private}'
    }


@pytest.mark.django_db
def test_unfollow_declined_valid_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_declined_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == {
        'detail': f'You canceled follow request to {user_2_private}'
    }


@pytest.mark.django_db
def test_unfollow_current_user(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_unfollow_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
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
        user,
        user_2,
        follower_user_accepted,
):
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user_2.id])
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
        user,
        user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(
        reverse(UNFOLLOW_URL, args=[user_2.id])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': f'You are not following {user_2}'
    }
