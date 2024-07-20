from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from apps.events.models.city import City
from apps.events.serializers.city import CityListSerializer


class CityViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    A simple ViewSet for viewing City data.
    """

    permission_classes = [AllowAny]
    queryset = City.objects.all()
    serializer_class = CityListSerializer

    @swagger_auto_schema(
        tags=['city'],
        operation_description="Get all city place_id",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
