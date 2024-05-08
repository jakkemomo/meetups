from django_filters import rest_framework as filters

from apps.profiles.models import User


class UserFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='exact', field_name='username')
    name_contains = filters.CharFilter(lookup_expr="icontains", field_name='username')

    age = filters.NumberFilter(lookup_expr='exact', field_name='age')
    age__gte = filters.NumberFilter(lookup_expr='gte', field_name='age')
    age__lte = filters.NumberFilter(lookup_expr='lte', field_name='age')

    city = filters.CharFilter(lookup_expr='exact', field_name='city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='city')

    class Meta:
        model = User
        fields = [
            'name',
            'name_contains',
            'age',
            'age__gte',
            'age__lte',
            'city',
            'city_in',
        ]
