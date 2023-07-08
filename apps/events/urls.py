from django.urls import include, path

from .views import EventCreation, EventDetail, EventEdition


urlpatterns = [
    # path('', EventListing.as_view(), name='index'),
    # path('<str:category_id>', EventListing.as_view(), name='category'),
    path('create/', EventCreation.as_view(), name='event_creation'),
    path('<str:pk>/', EventDetail.as_view(), name='detail'),
    path('<str:pk>/update/', EventCreation.as_view(), name='event_creation'),
]
