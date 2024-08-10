import pytest
from rest_framework.reverse import reverse

from apps.profiles.tests.followers.constants import PROFILE_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.django_db
def test_profile_get(api_client, user_with_categories, category):
    token = get_tokens(user_with_categories)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.get(reverse(PROFILE_URL, args=[user_with_categories.id]))

    assert response.status_code == 200
    assert response.json() == {
        "id": user_with_categories.id,
        "username": "user",
        "first_name": "Vlad",
        "last_name": "Pupkin",
        "email": "user@example.com",
        "city": {
            "id": 2495,
            "name": "Minsk",
            "display_name": "Minsk, Minsk City, Belarus",
            "country_id": 36,
            "latitude": "53.90000",
            "longitude": "27.56667",
            "timezone": "Europe/Minsk",
        },
        "image_url": "https://imgur.com/a/1C9U5",
        "is_email_verified": True,
        "is_private": False,
        "bio": "I like to play football",
        "category_favorite": [{"id": category.id, "name": "test_category", "image_url": None}],
        "date_of_birth": "2000-01-01",
        "gender": "MALE",
        "type": "INDIVIDUAL",
    }
