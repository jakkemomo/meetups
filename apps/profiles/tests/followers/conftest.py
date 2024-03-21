import pytest

from apps.profiles.models.followers import Follower


@pytest.fixture
def follower_user_accepted(user, user_2) -> Follower:
    data = {
        'user': user_2,
        'follower': user,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_accepted_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_pending_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_declined_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_2_private,
        'follower': user_private,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_accepted(user, user_2) -> Follower:
    data = {
        'user': user,
        'follower': user_2,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_accepted_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.ACCEPTED,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_pending_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.PENDING,
    }
    return Follower.objects.create(**data)


@pytest.fixture
def follower_user_2_declined_private(user_private, user_2_private) -> Follower:
    data = {
        'user': user_private,
        'follower': user_2_private,
        'status': Follower.Status.DECLINED,
    }
    return Follower.objects.create(**data)
