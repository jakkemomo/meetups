from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.profiles.models import User


class ReverifyEmailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("email",)


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=None, min_length=None, allow_blank=False)
