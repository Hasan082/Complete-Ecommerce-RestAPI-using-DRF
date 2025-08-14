from django.shortcuts import render
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from .pagination import StandardResultPagination


@extend_schema(
    tags=["Category"],
    summary="Category endpoint summary",
    description="Category Detailed description of what this API does."
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

@extend_schema(
    tags=["Products"],
    summary="Product endpoint summary",
    description="Product Detailed description of what this API does."
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = StandardResultPagination
    lookup_field = 'slug'
