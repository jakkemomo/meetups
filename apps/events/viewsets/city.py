from cities_light.contrib.restframework3 import CitiesLightListModelViewSet, City
from django.db.models import Q, Subquery
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework.decorators import action

from apps.events.filters import TrigramSimilaritySearchFilter
from apps.events.models import Event
from apps.events.serializers.city import CitySerializer


class CityViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """

    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [TrigramSimilaritySearchFilter, DjangoFilterBackend]
    search_fields = ["name", "display_name", "alternate_names"]

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset

        if self.action == "cities_with_events":
            queryset = queryset.filter(
                id__in=Subquery(
                    Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
                    .values_list("city_id", flat=True)
                    .distinct()
                    .order_by()
                )
            )

        return queryset

    @swagger_auto_schema(request_body=no_body)
    @action(
        methods=["get"],
        detail=False,
        permission_classes=[],
        url_path="available",
        url_name="cities_with_events",
    )
    def cities_with_events(self, request):
        return super().list(request)
