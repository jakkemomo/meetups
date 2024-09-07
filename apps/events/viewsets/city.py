from cities_light.contrib.restframework3 import CitiesLightListModelViewSet
from cities_light.contrib.restframework3 import City
from django.db.models import Q, ExpressionWrapper, F, FloatField
from django.db.models import Subquery
from django.db.models.functions.math import Sqrt
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import serializers
from rest_framework.decorators import action

from apps.events.filters import TrigramSimilaritySearchFilter, CityFilter
from apps.events.models import Event
from apps.events.serializers.city import CitySerializer

lat_param = openapi.Parameter(
    "lat",
    openapi.IN_QUERY,
    description="Latitude for coordinate filtering. Must be used together with 'lng'.",
    type=openapi.TYPE_NUMBER,
    required=False,
)

lng_param = openapi.Parameter(
    "lng",
    openapi.IN_QUERY,
    description="Longitude for coordinate filtering. Must be used together with 'lat'.",
    type=openapi.TYPE_NUMBER,
    required=False,
)


class CityViewSet(CitiesLightListModelViewSet):
    """
    ListRetrieveView for City.
    """

    serializer_class = CitySerializer
    queryset = City.objects.all()
    filter_backends = [TrigramSimilaritySearchFilter, DjangoFilterBackend]
    search_fields = ["name_ru", "name_en"]
    filterset_class = CityFilter

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(population__gt=100_000)

        if self.action == "cities_with_events":
            queryset = queryset.filter(
                id__in=Subquery(
                    Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
                    .values_list("city_id", flat=True)
                    .distinct()
                    .order_by()
                )
            )
        lat = self.request.query_params.get("lat")
        lng = self.request.query_params.get("lng")
        if lat and lng:
            # todo: update to use point field
            lat = float(lat)
            lng = float(lng)
            approximate_distance = 3  # Approximate range in degrees

            # Step 1: Filter cities within a rough distance range
            filtered_cities = queryset.filter(
                Q(latitude__range=(lat - approximate_distance, lat + approximate_distance))
                & Q(longitude__range=(lng - approximate_distance, lng + approximate_distance))
            )

            # Step 2: Annotate with accurate distance using Euclidean distance
            queryset = filtered_cities.annotate(
                distance=ExpressionWrapper(
                    Sqrt((F("latitude") - lat) ** 2 + (F("longitude") - lng) ** 2),
                    output_field=FloatField(),
                )
            ).order_by("distance")
        elif lat or lng:
            raise serializers.ValidationError(
                "Both 'lat' and 'lng' are required together for coordinates filtering."
            )

        return queryset

    @swagger_auto_schema(manual_parameters=[lat_param, lng_param], request_body=no_body)
    @action(
        methods=["get"],
        detail=False,
        permission_classes=[],
        url_path="available",
        url_name="cities_with_events",
    )
    def cities_with_events(self, request):
        return super().list(request)

    @swagger_auto_schema(manual_parameters=[lat_param, lng_param], request_body=no_body)
    def list(self, request):
        return super().list(request)
