from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny

from apps.core.serializers.register import RegisterResponseSerializer, RegisterSerializer
from apps.profiles.models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(
        responses={status.HTTP_201_CREATED: RegisterResponseSerializer}, tags=["auth"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
