import pytest
from rest_framework.exceptions import ErrorDetail
from rest_framework.reverse import reverse

from apps.events.tests.events.constants import EVENTS_IS_PARTICIPANT_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_event_is_participant_without_following(
    api_client, user, user_2, event_user_2_is_participant
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"][0].get("id") is not None
    assert response.data["results"][0].get("name") == event_user_2_is_participant.name


@pytest.mark.django_db
def test_event_is_participant_accepted(
    api_client, user, user_2, follower_user_accepted, event_user_2_is_participant
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"][0].get("id") is not None
    assert response.data["results"][0].get("name") == event_user_2_is_participant.name


@pytest.mark.django_db
def test_event_is_participant_without_following_private(
    api_client, user, user_2_private, event_user_2_is_participant_private
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_is_participant_accepted_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_accepted_private,
    event_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"][0].get("id") is not None
    assert response.data["results"][0].get("name") == event_user_2_is_participant_private.name


@pytest.mark.django_db
def test_event_is_participant_pending_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_pending_private,
    event_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_is_participant_declined_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_declined_private,
    event_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_private_is_participant_without_following(
    api_client, user, user_2, event_private_user_2_is_participant
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_event_private_is_participant_accepted(
    api_client, user, user_2, follower_user_accepted, event_private_user_2_is_participant
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_event_private_is_participant_without_following_private(
    api_client, user, user_2_private, event_private_user_2_is_participant_private
):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_private_is_participant_accepted_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_accepted_private,
    event_private_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"] == []


@pytest.mark.django_db
def test_event_private_is_participant_pending_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_pending_private,
    event_private_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_private_created_by_declined_private(
    api_client,
    user_private,
    user_2_private,
    follower_user_declined_private,
    event_private_user_2_is_participant_private,
):
    token = get_tokens(user_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2_private.id]))

    # assertions
    assert response.status_code == 403
    assert response.data == {
        "detail": ErrorDetail(
            string="You do not have permission to perform this action.", code="permission_denied"
        )
    }


@pytest.mark.django_db
def test_event_is_participant_current_user(api_client, user_2, event_user_2_is_participant):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"][0].get("id") is not None
    assert response.data["results"][0].get("name") == event_user_2_is_participant.name


@pytest.mark.django_db
def test_event_private_is_participant_current_user(
    api_client, user_2, event_private_user_2_is_participant
):
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 200
    assert response.data["results"][0].get("id") is not None
    assert response.data["results"][0].get("name") == event_private_user_2_is_participant.name


@pytest.mark.django_db
def test_event_is_participant_no_creds(api_client, user_2):
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[user_2.id]))

    # assertions
    assert response.status_code == 401
    assert response.data == {
        "detail": ErrorDetail(
            string="Authentication credentials were not provided.", code="not_authenticated"
        )
    }


@pytest.mark.django_db
def test_event_is_participant_user_not_found(api_client, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(EVENTS_IS_PARTICIPANT_URL, args=[100]))

    # assertions
    assert response.status_code == 404
    assert response.data == {"detail": ErrorDetail(string="User not found", code="error")}
