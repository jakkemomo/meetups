from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.events.models import Category
from apps.events.permissions import CategoriesPermissions
from apps.events.serializers import (
    CategoryCreateSerializer,
    CategoryListSerializer,
    CategoryRetrieveSerializer,
    CategoryUpdateSerializer,
    EmptySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing event Categories.
    """

    model = Category
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, CategoriesPermissions]
    lookup_url_kwarg = "category_id"
    http_method_names = ["post", "get", "put", "delete"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return CategoryRetrieveSerializer
            case "create":
                return CategoryCreateSerializer
            case "update":
                return CategoryUpdateSerializer
            case "list":
                return CategoryListSerializer
            case _:
                return EmptySerializer

    @swagger_auto_schema(request_body=no_body)
    @action(
        methods=["post"],
        detail=True,
        permission_classes=[IsAuthenticatedOrReadOnly, CategoriesPermissions],
        url_path="favorite",
        url_name="category_favorite_add",
    )
    def add_category_to_favorite(self, request, category_id: int):
        user = request.user
        category = Category.objects.get(id=category_id)
        user.category_favorite.add(category)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=no_body)
    @add_category_to_favorite.mapping.delete
    def delete_category_from_favorite(self, request, category_id: int):
        user = request.user
        category = Category.objects.get(id=category_id)
        user.category_favorite.remove(category)
        return Response(status=status.HTTP_200_OK)
