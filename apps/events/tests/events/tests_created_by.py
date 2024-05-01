import os
import django
import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.events.tests.events.constants import CREATED_BY_URL


@pytest.mark.django_db
def test_event_created_by_without_following(
        api_client,
        user,
        user_2,
        event_created_by_user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2.name


@pytest.mark.django_db
def test_event_created_by_accepted(
        api_client,
        user,
        user_2,
        follower_user_accepted,
        event_created_by_user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2.name


@pytest.mark.django_db
def test_event_created_by_without_following_private(
        api_client,
        user,
        user_2_private,
        event_created_by_user_2_private,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2_private.name


@pytest.mark.django_db
def test_event_created_by_accepted_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_accepted_private,
        event_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2_private.name


@pytest.mark.django_db
def test_event_created_by_pending_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_pending_private,
        event_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2_private.name


@pytest.mark.django_db
def test_event_created_by_declined_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_declined_private,
        event_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2_private.name


@pytest.mark.django_db
def test_event_not_visible_created_by_without_following(
        api_client,
        user,
        user_2,
        event_not_visible_created_by_user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_not_visible_created_by_accepted(
        api_client,
        user,
        user_2,
        follower_user_accepted,
        event_not_visible_created_by_user_2,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_not_visible_created_by_accepted_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_accepted_private,
        event_not_visible_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_not_visible_created_by_pending_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_pending_private,
        event_not_visible_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_not_visible_created_by_declined_private(
        api_client,
        user_private,
        user_2_private,
        follower_user_declined_private,
        event_not_visible_created_by_user_2_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_created_by_current_user(
        api_client,
        user_2,
        event_created_by_user_2,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2.name


@pytest.mark.django_db
def test_event_not_visible_created_by_current_user(
        api_client,
        user_2,
        event_not_visible_created_by_user_2,
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_not_visible_created_by_user_2.name


@pytest.mark.django_db
def test_event_created_by_no_creds(
        api_client,
        user_2,
        event_created_by_user_2,
):
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2.name


@pytest.mark.django_db
def test_event_created_by_no_creds_private(
        api_client,
        user_2_private,
        event_created_by_user_2_private,
):
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data[0].get("id") is not None
    assert response.data[0].get("name") == event_created_by_user_2_private.name


@pytest.mark.django_db
def test_event_not_visible_created_by_no_creds(
        api_client,
        user_2,
        event_not_visible_created_by_user_2,
):
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_not_visible_created_by_no_creds_private(
        api_client,
        user_2_private,
        event_not_visible_created_by_user_2_private,
):
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[user_2_private.id])
    )
    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_event_created_by_user_not_found(
        api_client,
        user,
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(
        reverse(CREATED_BY_URL, args=[100])
    )
    assert response.status_code == 404
    assert response.data == {
        'detail': ErrorDetail(string='User not found', code='error')
    }
