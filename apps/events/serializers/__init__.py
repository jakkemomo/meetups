from .tags import (
    TagCreateSerializer,
    TagRetrieveSerializer,
    TagUpdateSerializer,
    TagListSerializer,
)
from .events import (
    EventCreateSerializer,
    EventUpdateSerializer,
    EventRetrieveSerializer,
    EventListSerializer,
    EventRegisterSerializer,
    EventFavoriteAddSerializer,
    EventFavoriteDeleteSerializer,
)
from .ratings import (
    RatingCreateSerializer,
    RatingRetrieveSerializer,
    RatingUpdateSerializer,
    RatingListSerializer,
)
from .map import GeoJsonSerializer
