import pytest
from rest_framework.reverse import reverse

from apps.profiles.models import User
from apps.profiles.models.followers import Follower
from apps.profiles.tests.followers.constants import UPDATE_URL
from apps.profiles.tests.utils import get_tokens


@pytest.mark.usefixtures(
    "follower_user_pending_private",
)
@pytest.mark.django_db
def test_patch_is_private_false_pending(
        api_client,
        user_2_private,
):
    data = {"is_private": False}
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.patch(
        path=reverse(UPDATE_URL, args=[user_2_private.id]),
        data=data
    )
    user_2_private = User.objects.filter(id=user_2_private.id).first()

    assert response.status_code == 200
    assert user_2_private.is_private is False
    assert Follower.objects.filter(user=user_2_private).first().status == Follower.Status.ACCEPTED


@pytest.mark.usefixtures(
    "follower_user_declined_private",
)
@pytest.mark.django_db
def test_patch_is_private_false_declined(
        api_client,
        user_2_private,
):
    data = {"is_private": False}
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.patch(
        path=reverse(UPDATE_URL, args=[user_2_private.id]),
        data=data
    )
    user_2_private = User.objects.filter(id=user_2_private.id).first()

    assert response.status_code == 200
    assert user_2_private.is_private is False
    assert Follower.objects.filter(user=user_2_private).first() is not True


@pytest.mark.usefixtures(
    "follower_user_accepted_private",
)
@pytest.mark.django_db
def test_patch_is_private_false_accepted(
        api_client,
        user_2_private,
):
    data = {"is_private": False}
    token = get_tokens(user_2_private)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.patch(
        path=reverse(UPDATE_URL, args=[user_2_private.id]),
        data=data
    )
    user_2_private = User.objects.filter(id=user_2_private.id).first()

    assert response.status_code == 200
    assert user_2_private.is_private is False
    assert Follower.objects.filter(user=user_2_private).first().status == Follower.Status.ACCEPTED


@pytest.mark.usefixtures(
    "follower_user_accepted",
)
@pytest.mark.django_db
def test_patch_is_private_true_accepted(
        api_client,
        user_2,
):
    data = {"is_private": True}
    token = get_tokens(user_2)
    api_client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    response = api_client.patch(
        path=reverse(UPDATE_URL, args=[user_2.id]),
        data=data
    )
    user_2 = User.objects.filter(id=user_2.id).first()

    assert response.status_code == 200
    assert user_2.is_private is True
    assert Follower.objects.filter(user=user_2).first().status == Follower.Status.ACCEPTED
