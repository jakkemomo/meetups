from django.urls import include, path

from .views import EventCreation, EventDetail, EventEdition, EventListing


urlpatterns = [
    path('list/', EventListing.as_view(), name='list'),
    path('create/', EventCreation.as_view(), name='event_creation'),
    path('<str:pk>/', EventDetail.as_view(), name='detail'),
    path('<str:pk>/update/', EventEdition.as_view(), name='event_creation'),
]
