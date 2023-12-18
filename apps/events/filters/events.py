from django_filters import CharFilter, IsoDateTimeFilter, FilterSet

from apps.events.models import Event


class EventFilter(FilterSet):
    tag = CharFilter(field_name='tags__name', lookup_expr='iexact')
    date_from = IsoDateTimeFilter(field_name='start_date', lookup_expr='gte')
    date_to = IsoDateTimeFilter(field_name='start_date', lookup_expr='lte')

    class Meta:
        model = Event
        fields: list[str] = []
