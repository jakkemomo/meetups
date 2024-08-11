import pytest
from rest_framework.reverse import reverse

from apps.notifications.tests.constants import EMAIL_PREFERENCES_GET_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_email_notifications_preferences_patch_valid(api_client, user):
    # user logs in
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    # user gets his notifications preferences
    data = {
        "system": False,
        "event_start": False,
        "new_invite_to_event": False,
        "new_interesting_event_near": False,
        "new_following_user_event": False,
        "following_user_near_going_to_event": False,
    }
    response = api_client.patch(reverse(EMAIL_PREFERENCES_GET_URL), data=data)

    # assertions
    assert response.status_code == 200
    assert response.data == data


@pytest.mark.django_db
def test_email_notifications_preferences_patch_unauthorized(api_client, user):
    # user gets his notifications preferences
    data = {
        "system": False,
        "event_start": False,
        "new_invite_to_event": False,
        "new_interesting_event_near": False,
        "new_following_user_event": False,
        "following_user_near_going_to_event": False,
    }
    response = api_client.patch(reverse(EMAIL_PREFERENCES_GET_URL), data=data)

    # assertions
    assert response.status_code == 401


@pytest.mark.django_db
def test_email_notifications_preferences_patch_invalid_data(api_client, user):
    # user logs in
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    # user gets his notifications preferences
    data = {"system": 123}
    response = api_client.put(reverse(EMAIL_PREFERENCES_GET_URL), data=data)

    # assertions
    assert response.status_code == 400
