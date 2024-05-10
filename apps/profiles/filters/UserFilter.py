from django_filters import rest_framework as filters

from apps.profiles.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'username': ['exact', 'icontains'],
            'age': ['exact', 'gte', 'lte'],
            'city': ['exact', 'in'],
        }
