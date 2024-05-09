import json

from django.core.serializers import serialize
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.events.models import Event
from apps.events.serializers import GeoJsonSerializer


class MarkerViewSet(mixins.ListModelMixin, GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Event.objects.filter(Q(is_visible=True) & Q(is_finished=False))
    serializer_class = GeoJsonSerializer

    @swagger_auto_schema(
        tags=['map'],
        operation_description="Get all events in GeoJSON format",
    )
    def list(self, request, *args, **kwargs):
        geo_events = json.loads(
            serialize(
                "geojson", self.queryset.all(),
                geometry_field="location",
                fields=["id", "name", "start_date", "end_date", "description", "address"])
        )
        return Response(geo_events, status=status.HTTP_200_OK)
