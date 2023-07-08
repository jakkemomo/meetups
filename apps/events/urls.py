from django.urls import include, path

from .views import EventCreation, EventListing, EventDetail


urlpatterns = [
    path('/', EventListing.as_view(), name='index'),
    # path('<str:category_id>', EventListing.as_view(), name='category'),
    path('<str:event_id>/', EventDetail.as_view(), name='detail'),
    path('create/', EventCreation.as_view(), name='event_creation'),
    path('<str:event_id>/update/', EventCreation.as_view(), name='event_creation'),
]
