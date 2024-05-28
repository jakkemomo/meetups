from rest_framework import serializers

from apps.events.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    image_url = serializers.CharField(max_length=60, required=False)

    class Meta:
        model = Category
        fields = ["id", "name", "image_url"]


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "image_url"]


class CategoryUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30)
    image_url = serializers.CharField(max_length=60, required=False)

    class Meta:
        model = Category
        fields = ["id", "name", "image_url"]


class CategoryListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=30)
    image_url = serializers.CharField(max_length=60, required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ["id", "name", "image_url"]
