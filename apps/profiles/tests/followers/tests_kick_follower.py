import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.followers.constants import KICK_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.usefixtures("follower_user_accepted_kick")
@pytest.mark.django_db
def test_kick_follower_valid(api_client, user, user_2):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(KICK_URL, args=[user_2.id]))
    print(response.data)
    assert response.status_code == 200
    assert response.data == {"detail": "User is no longer following you"}


@pytest.mark.django_db
def test_kick_follower_no_creds(api_client, user_2):
    response = api_client.delete(reverse(KICK_URL, args=[user_2.id]))
    assert response.status_code == 401
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_kick_follower_user_not_found(api_client, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(KICK_URL, args=[100]))
    assert response.status_code == 404
    assert response.data == {"detail": "User not found"}


@pytest.mark.django_db
def test_kick_follower_not_following(api_client, user, user_2):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.delete(reverse(KICK_URL, args=[user_2.id]))
    assert response.status_code == 404
    assert response.data == {"detail": "User is not following you"}
