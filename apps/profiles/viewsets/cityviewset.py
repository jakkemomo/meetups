from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from apps.profiles.models import City
from apps.profiles.serializers import CitySerializer


class CityViewSet(viewsets.ModelViewSet):
    model = City
    queryset = City.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CitySerializer
    http_method_names = ["get", "put", "patch", "delete", ]
    lookup_url_kwarg = "user_id"
