import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.utils import get_tokens
from apps.profiles.tests.followers.constants import UPDATE_URL


@pytest.mark.django_db
def test_profile_get(api_client, user):
    token = get_tokens(user)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(UPDATE_URL, args=[user.id]))

    assert response.status_code == 200
