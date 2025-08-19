from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets, filters
from .pagination import StandardResultPagination
from common.permission import IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter, ProductSearchOrderingMixin
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Category"],
    summary="Category endpoint summary",
    description="Category Detailed description of what this API does.",
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = "slug"


@extend_schema(
    tags=["Products"],
    summary="Product endpoint summary",
    description="Product Detailed description of what this API does.",
)
class ProductViewSet(ProductSearchOrderingMixin, viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = StandardResultPagination
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    
    
    # ProductSearchOrderingMixin ,ade in filters.py file and ProductFilter also 
    # in same file and filter_backends must be call ebfore filterset_class