from django.contrib.gis.geos import Polygon, Point
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.profiles.models import CityLocation
from apps.profiles.serializers import CitySerializer


def area_bbox(location: dict):
    """
    Return Poligon area approximately 1 km radius around specified koordinates
    """
    r = 0.01
    min_lat = float(location['latitude']) - r
    max_lat = float(location['latitude']) + r
    min_lng = float(location['longitude']) - r
    max_lng = float(location['longitude']) + r

    bbox = (min_lng, min_lat, max_lng, max_lat)
    return Polygon.from_bbox(bbox)


class CityViewSet(viewsets.ModelViewSet):
    model = CityLocation
    queryset = CityLocation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CitySerializer
    http_method_names = ["get", "put", "post", "delete", ]

    def create(self, request, *args, **kwargs):
        if self.queryset.filter(location__within=area_bbox(request.data['location'])):
            return Response(status=status.HTTP_409_CONFLICT, data=['This city already exist'])
        return super().create(request, args, kwargs)
