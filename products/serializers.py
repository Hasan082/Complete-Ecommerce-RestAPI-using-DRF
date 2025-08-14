from .models import Category, Product
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    stock_status = serializers.SerializerMethodField()
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "image_url",
            "price",
            "discount_percentage",
            "discounted_price",
            "stock",
            "stock_status",
            "is_active",
            "category",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "slug",
            "discounted_price",
            "stock_status",
            "category",
            "created_at",
            "updated_at",
        ]

    def get_stock_status(self, obj):
        return obj.stock_status()
