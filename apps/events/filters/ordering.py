from rest_framework.filters import OrderingFilter


class DistinctOrderingFilter(OrderingFilter):
    def filter_queryset(self, request, queryset, view):
        queryset = super().filter_queryset(request, queryset, view)
        return queryset.distinct()
