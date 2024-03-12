import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.fixtures import *
from apps.profiles.tests.followers.constants import FOLLOW_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_follow_valid(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user_2.id])
    )
    assert response.status_code == 201
    assert response.data.get('id') is not None
    assert response.data.get('user') == user_2.id
    assert response.data.get('follower') == user.id
    assert response.data.get('status') == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_follow_valid_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user_2_private.id])
    )
    assert response.status_code == 201
    assert response.data.get('id') is not None
    assert response.data.get('user') == user_2_private.id
    assert response.data.get('follower') == user.id
    assert response.data.get('status') == Follower.Status.PENDING


@pytest.mark.django_db
def test_follow_current_user(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(string='This is a current user', code='error')
    }


@pytest.mark.django_db
def test_follow_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
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
        user,
):
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user.id])
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
        user,
        user_2,
        follower_user_accepted,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user_2.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Already following'}


@pytest.mark.django_db
def test_follow_pending_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_pending_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user_2_private.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Follow request already sent'}


@pytest.mark.django_db
def test_follow_declined(
        api_client,
        user_private,
        user_2_private,
        follower_user_declined_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.post(
        reverse(FOLLOW_URL, args=[user_2_private.id])
    )
    assert response.status_code == 409
    assert response.data == {'detail': 'Follow request already sent'}
