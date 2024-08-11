import pytest
from rest_framework.reverse import reverse

from apps.notifications.tests.constants import IN_APP_PREFERENCES_GET_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_in_app_notifications_preferences_get_valid(api_client, user):
    # user logs in
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    # user gets his notifications preferences
    response = api_client.get(reverse(IN_APP_PREFERENCES_GET_URL))

    # assertions
    assert response.status_code == 200
    assert response.data == {
        "user": user.id,
        "system": user.in_app_notifications_preferences.system,
        "new_message": user.in_app_notifications_preferences.new_message,
        "new_follower": user.in_app_notifications_preferences.new_follower,
        "new_follow_request": user.in_app_notifications_preferences.new_follow_request,
        "accepted_follow_request": user.in_app_notifications_preferences.accepted_follow_request,
        "event_start": user.in_app_notifications_preferences.event_start,
        "new_invite_to_event": user.in_app_notifications_preferences.new_invite_to_event,
        "new_interesting_event_near": user.in_app_notifications_preferences.new_interesting_event_near,
        "new_following_user_event": user.in_app_notifications_preferences.new_following_user_event,
        "following_user_near_going_to_event": user.in_app_notifications_preferences.following_user_near_going_to_event,
    }


@pytest.mark.django_db
def test_in_app_notifications_preferences_get_unauthorized(api_client, user):
    # user gets his notifications preferences
    response = api_client.get(reverse(IN_APP_PREFERENCES_GET_URL))

    # assertions
    assert response.status_code == 401
