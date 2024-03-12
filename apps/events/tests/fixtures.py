import pytest

from apps.events.models.events import Event
from apps.profiles.tests.fixtures import *


@pytest.fixture
def event() -> Event:
    return Event.objects.create(
        name="test_event",
    )


@pytest.fixture
def event_not_visible() -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
    )


@pytest.fixture
def event_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2,
    )


@pytest.fixture
def event_not_visible_created_by_user_2(user_2) -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
        created_by=user_2,
    )


@pytest.fixture
def event_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        created_by=user_2_private,
    )


@pytest.fixture
def event_not_visible_created_by_user_2_private(user_2_private) -> Event:
    return Event.objects.create(
        name="test_event",
        is_visible=False,
        created_by=user_2_private,
    )


@pytest.fixture
def event_user_2_is_participant(user_2, event) -> Event:
    event.participants.add(user_2.id)
    event.save()
    return event


@pytest.fixture
def event_user_2_is_participant_private(user_2_private, event) -> Event:
    event.participants.add(user_2_private.id)
    event.save()
    return event


@pytest.fixture
def event_not_visible_user_2_is_participant(user_2, event_not_visible) -> Event:
    event_not_visible.participants.add(user_2.id)
    event_not_visible.save()
    return event_not_visible


@pytest.fixture
def event_not_visible_user_2_is_participant_private(user_2_private, event_not_visible) -> Event:
    event_not_visible.participants.add(user_2_private.id)
    event_not_visible.save()
    return event_not_visible
