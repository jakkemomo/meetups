from django_filters import rest_framework as filters

from apps.profiles.models.followers import Follower


class UserFollowersFilter(filters.FilterSet):
    """ Setting filter for searching user's followers"""
    username = filters.CharFilter(lookup_expr='exact', field_name='follower__username')
    username_contains = filters.CharFilter(lookup_expr='icontains', field_name='follower__username')
    date_of_birth = filters.DateFilter(lookup_expr='exact', field_name='follower__date_of_birth')
    date_of_birth__gte = filters.DateFilter(lookup_expr='gte', field_name='follower__date_of_birth')
    date_of_birth__lte = filters.DateFilter(lookup_expr='lte', field_name='follower__date_of_birth')
    city = filters.CharFilter(lookup_expr='exact', field_name='follower__city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='follower__city')
    gender = filters.CharFilter(lookup_expr='exact', field_name='follower__gender')
    gender_contains = filters.CharFilter(lookup_expr='icontains', field_name='follower__gender')
    type = filters.CharFilter(lookup_expr='exact', field_name='follower__type')
    type_contains = filters.CharFilter(lookup_expr='icontains', field_name='follower__type')

    class Meta:
        model = Follower
        fields = [
            'username',
            'username_contains',
            'date_of_birth',
            'date_of_birth__gte',
            'date_of_birth__lte',
            'city',
            'city_in',
            'gender',
            'gender_contains',
            'type',
            'type_contains',
        ]


class UserFollowsFilter(filters.FilterSet):
    """ Setting filter of users who is current user follows """
    username = filters.CharFilter(lookup_expr='exact', field_name='user__username')
    username_contains = filters.CharFilter(lookup_expr='icontains', field_name='user__username')
    date_of_birth = filters.DateFilter(lookup_expr='exact', field_name='user__date_of_birth')
    date_of_birth__gte = filters.DateFilter(lookup_expr='gte', field_name='user__date_of_birth')
    date_of_birth__lte = filters.DateFilter(lookup_expr='lte', field_name='user__date_of_birth')
    city = filters.CharFilter(lookup_expr='exact', field_name='user__city')
    city_in = filters.CharFilter(lookup_expr='in', field_name='user__city')
    gender = filters.CharFilter(lookup_expr='exact', field_name='user__gender')
    gender_contains = filters.CharFilter(lookup_expr='icontains', field_name='user__gender')
    type = filters.CharFilter(lookup_expr='exact', field_name='user__type')
    type_contains = filters.CharFilter(lookup_expr='icontains', field_name='user__type')

    class Meta:
        model = Follower
        fields = [
            'username',
            'username_contains',
            'date_of_birth',
            'date_of_birth__gte',
            'date_of_birth__lte',
            'city',
            'city_in',
            'gender',
            'gender_contains',
            'type',
            'type_contains',
        ]
