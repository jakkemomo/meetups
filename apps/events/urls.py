from django.urls import include, path

from .views import EventCreation, EventListing, EventDetail


urlpatterns = [
    path('', EventListing.as_view(), name='index'),
    path('<int:category_id>', EventListing.as_view(), name='category'),
    path('<int:event_id>', EventDetail.as_view(), name='detail'),
    path('', EventCreation.as_view(), name='event_creation')
]
