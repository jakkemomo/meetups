from django_filters import rest_framework as filters

from apps.events.models import Event, Tag, Category


class EventFilter(filters.FilterSet):
    name_contains = filters.CharFilter(lookup_expr='icontains', field_name='name')
    name = filters.CharFilter(lookup_expr='exact', field_name='name')

    start_date = filters.DateFilter(lookup_expr='exact', field_name='start_date')
    start_date_gte = filters.DateFilter(lookup_expr='gte', field_name='start_date')
    start_date_lte = filters.DateFilter(lookup_expr='lte', field_name='start_date')

    end_date = filters.DateFilter(lookup_expr='exact', field_name='end_date')
    end_date_gte = filters.DateFilter(lookup_expr='gte', field_name='end_date')
    end_date_lte = filters.DateFilter(lookup_expr='lte', field_name='end_date')

    average_rating = filters.NumberFilter(lookup_expr='exact', field_name='average_rating')
    average_rating__gte = filters.NumberFilter(lookup_expr='gte', field_name='average_rating')
    average_rating__lte = filters.NumberFilter(lookup_expr='lte', field_name='average_rating')

    tags = filters.CharFilter(lookup_expr='exact', field_name='tags')
    tags_in = filters.ModelMultipleChoiceFilter(field_name='tags', queryset=Tag.objects.all(),
                                                conjoined=False)

    category = filters.CharFilter(lookup_expr='iexact', field_name='category')
    category_in = filters.ModelMultipleChoiceFilter(field_name='category', queryset=Category.objects.all(),
                                                    conjoined=False)

    city = filters.CharFilter(lookup_expr='exact', field_name='city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='city')

    free = filters.BooleanFilter(lookup_expr='exact', field_name='price')

    participants_age = filters.NumberFilter(lookup_expr='exact', field_name='participants_age')
    participants_age__gte = filters.NumberFilter(lookup_expr='gte', field_name='participants_age')
    participants_age__lte = filters.NumberFilter(lookup_expr='lte', field_name='participants_age')

    class Meta:
        model = Event
        fields = [
            'name_contains',
            'name',
            'start_date',
            'start_date_gte',
            'start_date_lte',
            'end_date',
            'end_date_gte',
            'end_date_lte',
            'average_rating',
            'average_rating__gte',
            'average_rating__lte',
            'tags',
            'tags_in',
            'category',
            'category_in',
            'city',
            'city_in',
            'free',
            'participants_age',
            'participants_age__gte',
            'participants_age__lte'
        ]
