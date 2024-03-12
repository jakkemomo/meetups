import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.fixtures import *
from apps.profiles.tests.followers.constants import LIST_FOLLOWING_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_list_following_without_following(
        api_client,
        user,
        user_2,
        follower_user_2_accepted,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == user.id
    assert response.data[0].get("follower") == user_2.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_accepted(
        api_client,
        user,
        user_2,
        follower_user_accepted,
        follower_user_2_accepted,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == user.id
    assert response.data[0].get("follower") == user_2.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_accepted_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_accepted_private,
        follower_user_2_accepted_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == user_private.id
    assert response.data[0].get("follower") == user_2_private.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_without_following_private(
        api_client,
        user_private,
        user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.django_db
def test_list_following_pending_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_pending_private,
        follower_user_2_accepted_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2_private.id])
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
        user_private,
        user_2_private,
        follower_user_declined_private,
        follower_user_2_accepted_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2_private.id])
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
        user,
        user_2,
        follower_user_2_accepted,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("user") == user.id
    assert response.data[0].get("follower") == user_2.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_following_current_user_pending_private(
        api_client,
        user_private,
        user_2,
        follower_user_2_pending_private,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_following_current_user_declined_private(
        api_client,
        user_private,
        user_2,
        follower_user_2_declined_private,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_following_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
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
        user,
):
    response = api_client.get(
        reverse(LIST_FOLLOWING_URL, args=[user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }

