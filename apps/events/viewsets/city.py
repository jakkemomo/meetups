from cities_light.contrib.restframework3 import CitiesLightListModelViewSet, City
from django_filters.rest_framework import DjangoFilterBackend

from apps.events.filters import TrigramSimilaritySearchFilter
from apps.events.serializers.city import CitySerializer


class CityViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """
    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [TrigramSimilaritySearchFilter, DjangoFilterBackend]
    search_fields = ["name", "display_name", "alternate_names",]

    def get_queryset(self):
        queryset = self.queryset
        return queryset
