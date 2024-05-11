from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny

from apps.events.models import Currency
from apps.events.serializers import CurrencySerializer


class CurrencyViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Only get method is allowed for this viewset"""

    permission_classes = [AllowAny]
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer

    @swagger_auto_schema(
        tags=['currency'],
        operation_description="Get all currencies",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
