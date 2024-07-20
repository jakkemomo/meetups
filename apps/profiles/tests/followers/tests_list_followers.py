import pytest
from rest_framework.reverse import reverse
from rest_framework.exceptions import ErrorDetail

from apps.profiles.tests.utils import get_tokens
from apps.profiles.tests.followers.constants import LIST_FOLLOWERS_URL
from apps.profiles.models.followers import Follower


@pytest.mark.django_db
def test_list_followers_without_following(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.usefixtures(
    "follower_user_accepted",
)
@pytest.mark.django_db
def test_list_followers_accepted(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("user")["id"] == user_2.id
    assert response.data[0].get("follower")["id"] == user.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.usefixtures(
    "follower_user_accepted_private",
)
@pytest.mark.django_db
def test_list_followers_accepted_private(
        api_client,
        user_private,
        user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("user")["id"] == user_2_private.id
    assert response.data[0].get("follower")["id"] == user_private.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.django_db
def test_list_followers_without_following_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.usefixtures(
    "follower_user_pending_private",
)
@pytest.mark.django_db
def test_list_followers_pending_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.usefixtures(
    "follower_user_declined_private",
)
@pytest.mark.django_db
def test_list_followers_declined_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 403
    assert response.data == {
        'detail': ErrorDetail(
            string='You do not have permission to perform this action.',
            code='permission_denied'
        )
    }


@pytest.mark.usefixtures(
    "follower_user_accepted",
)
@pytest.mark.django_db
def test_list_followers_current_user_accepted(
        api_client,
        user,
        user_2,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("user")["id"] == user_2.id
    assert response.data[0].get("follower")["id"] == user.id
    assert response.data[0].get("status") == Follower.Status.ACCEPTED


@pytest.mark.usefixtures(
    "follower_user_pending_private",
)
@pytest.mark.django_db
def test_list_followers_current_user_pending_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.usefixtures(
    "follower_user_declined_private",
)
@pytest.mark.django_db
def test_list_followers_current_user_declined_private(
        api_client,
        user,
        user_2_private,
):
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_list_followers_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }


@pytest.mark.django_db
def test_list_followers_no_creds(
        api_client,
        user,
):
    response = api_client.get(
        reverse(LIST_FOLLOWERS_URL, args=[user.id])
    )
    assert response.status_code == 401
    assert response.data == {
        'detail': ErrorDetail(
            string='Authentication credentials were not provided.',
            code='not_authenticated',
        )
    }
