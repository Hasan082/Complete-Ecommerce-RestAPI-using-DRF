import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    in_stock = django_filters.BooleanFilter(field_name="stock", lookup_expr='gt')
    
    class Meta:
        model = Product
        fields = ['category', 'min_price', 'max_price', 'in_stock']
        
        
class ProductSearchOrderingMixin:
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'discounted_price']
    ordering = ['-created_at']