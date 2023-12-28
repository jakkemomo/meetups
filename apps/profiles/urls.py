from django.urls import path, include


from .viewsets import UserRatingViewSet
from rest_framework import routers

app_name = "profiles"

router = routers.SimpleRouter()
router.register('user_ratings', UserRatingViewSet)

urlpatterns = [
    path("api/v1/user/(?P<user_id>[^/.]+)/", include(router.urls)),
]
