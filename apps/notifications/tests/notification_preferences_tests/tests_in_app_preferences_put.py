import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens
from apps.notifications.tests.constants import IN_APP_PREFERENCES_GET_URL


@pytest.mark.django_db
def test_in_app_notifications_preferences_put_valid(
        api_client,
        user,
):
    # user logs in
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    # user gets his notifications preferences
    data = {
        "system": False,
        "new_message": False,
        "new_follower": False,
        "new_follow_request": False,
        "accepted_follow_request": False,
        "event_start": False,
        "new_invite_to_event": False,
        "new_interesting_event_near": False,
        "new_following_user_event": False,
        "following_user_near_going_to_event": False
    }
    response = api_client.put(
        reverse(IN_APP_PREFERENCES_GET_URL),
        data=data
    )

    # assertions
    assert response.status_code == 200
    assert response.data == data


@pytest.mark.django_db
def test_in_app_notifications_preferences_put_unauthorized(
        api_client,
        user,
):
    # user gets his notifications preferences
    data = {
        "system": False,
        "new_message": False,
        "new_follower": False,
        "new_follow_request": False,
        "accepted_follow_request": False,
        "event_start": False,
        "new_invite_to_event": False,
        "new_interesting_event_near": False,
        "new_following_user_event": False,
        "following_user_near_going_to_event": False
    }
    response = api_client.put(
        reverse(IN_APP_PREFERENCES_GET_URL),
        data=data
    )

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db
def test_in_app_notifications_preferences_put_invalid_data(
        api_client,
        user,
):
    # user logs in
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    # user gets his notifications preferences
    data = {
        "system": 123,
    }
    response = api_client.put(
        reverse(IN_APP_PREFERENCES_GET_URL),
        data=data
    )

    # assertions
    assert response.status_code == 400
