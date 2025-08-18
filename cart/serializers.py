from rest_framework import serializers
from .models import Cart, CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    product_discounted_price = serializers.DecimalField(
        source='product.discounted_price', max_digits=10, decimal_places=2, read_only=True
    )
    item_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = CartItem
        fields = [
            'id',
            'product',
            'product_title',
            'product_price',
            'product_discounted_price',
            'quantity',
            'item_total',
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total_discount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    is_anonymous = serializers.BooleanField(read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'session_key',
            'created_at',
            'updated_at',
            'is_anonymous',
            'total_items',
            'subtotal',
            'total_discount',
            'total',
            'items',
        ]


# {
#   "id": 1,
#   "user": 5,
#   "session_key": null,
#   "total_items": 3,
#   "subtotal": "240.00",
#   "total_discount": "60.00",
#   "total": "240.00",
#   "items": [
#     {
#       "id": 1,
#       "product": 10,
#       "product_title": "T-Shirt",
#       "product_price": "100.00",
#       "product_discounted_price": "80.00",
#       "quantity": 2,
#       "item_total": "160.00"
#     },
#     {
#       "id": 2,
#       "product": 11,
#       "product_title": "Jeans",
#       "product_price": "120.00",
#       "product_discounted_price": "120.00",
#       "quantity": 1,
#       "item_total": "120.00"
#     }
#   ]
# }
