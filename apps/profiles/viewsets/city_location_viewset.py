from django.contrib.gis.geos import Point
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.profiles.models import CityLocation
from apps.profiles.serializers import CityLocationSerializer


class CityLocationViewSet(viewsets.ModelViewSet):
    model = CityLocation
    queryset = CityLocation.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CityLocationSerializer
    http_method_names = ["get", "put", "post", "delete", ]

    def create(self, request, *args, **data):
        location = Point (request.data["location"]["longitude"], request.data["location"]["latitude"])
        if CityLocation.objects.filter(location=location).exists():
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().create(request, data)
