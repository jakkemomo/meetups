from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django.utils.translation import gettext_lazy as _
from rest_framework.filters import SearchFilter
from rest_framework.settings import api_settings


class TrigramSimilaritySearchFilter(SearchFilter):
    search_param = api_settings.SEARCH_PARAM
    search_title = _('Search')
    search_description = _('A search term.')

    def get_trigram_similarity(self, view, request):
        return getattr(view, 'trigram_similarity', 0.3)

    def get_search_terms(self, request):
        """
        Search terms are set by a ?search=... query parameter,
        and may be comma and/or whitespace delimited.
        """
        params = request.query_params.get(self.search_param, '')
        params = params.replace('\x00', '')  # strip null characters
        params = params.replace(',', ' ')
        return params.split()

    def get_search_fields(self, view, request):
        """
        Search fields are obtained from the view, but the request is always
        passed to this method. Sub-classes can override this method to
        dynamically change the search fields based on request content.
        """
        return getattr(view, 'search_fields', None)

    def filter_queryset(self, request, queryset, view):
        trigram_similarity = self.get_trigram_similarity(view, request)
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        # if no search_terms return
        if not search_terms:
            return queryset

        # make conditions
        conditions = []
        for search_term in search_terms:
            conditions.extend([
                TrigramSimilarity(field, search_term) for field in search_fields
            ])

        # take the greatest similarity from all conditions
        # and annotate as similarity
        return queryset.annotate(
            similarity=Greatest(*conditions)
        ).filter(similarity__gte=trigram_similarity)
