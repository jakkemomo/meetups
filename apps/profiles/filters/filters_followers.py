from django_filters import rest_framework as filters

from apps.profiles.models.followers import Follower


class UserFollowersFilter(filters.FilterSet):
    """ Setting filter for searching user's followers"""
    username = filters.CharFilter(lookup_expr='exact', field_name='follower__username')
    username_contains = filters.CharFilter(lookup_expr='icontains', field_name='follower__username')
    age = filters.NumberFilter(lookup_expr='exact', field_name='follower__age')
    age__gte = filters.NumberFilter(lookup_expr='gte', field_name='follower__age')
    age__lte = filters.NumberFilter(lookup_expr='lte', field_name='follower__age')
    city = filters.CharFilter(lookup_expr='exact', field_name='follower__city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='follower__city')

    class Meta:
        model = Follower
        fields = [
            'username',
            'username_contains',
            'age',
            'age__gte',
            'age__lte',
            'city',
            'city_in',
        ]


class UserFollowsFilter(filters.FilterSet):
    """ Setting filter of users who is current user follows """
    username = filters.CharFilter(lookup_expr='exact', field_name='user__username')
    username_contains = filters.CharFilter(lookup_expr='icontains', field_name='user__username')
    age = filters.NumberFilter(lookup_expr='exact', field_name='user__age')
    age__gte = filters.NumberFilter(lookup_expr='gte', field_name='user__age')
    age__lte = filters.NumberFilter(lookup_expr='lte', field_name='user__age')
    city = filters.CharFilter(lookup_expr='exact', field_name='user__city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='user__city')

    class Meta:
        model = Follower
        fields = [
            'username',
            'username_contains',
            'age',
            'age__gte',
            'age__lte',
            'city',
            'city_in',
        ]
