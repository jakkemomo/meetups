from django_filters import rest_framework as filters

from apps.profiles.models.followers import Follower


class UserFollowersFilter(filters.FilterSet):
    class Meta:
        model = Follower
        fields = {
            'user__username': ['exact', 'icontains'],
            'user__age': ['exact', 'gte', 'lte'],
            'user__city': ['exact', 'in'],
        }
