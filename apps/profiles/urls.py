from django.urls import path, include


from .viewsets import UserRatingViewSet
from rest_framework import routers

app_name = "profiles"

router = routers.SimpleRouter()
router.register('user/(?P<user_id>[^/.]+)/user_ratings', UserRatingViewSet, basename="UserRating")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
