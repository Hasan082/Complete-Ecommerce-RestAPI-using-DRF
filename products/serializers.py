from .models import Category, Product
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Category
        fields = '__all__'
        
        
class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'slug': {'read_only': True}
        }
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['discount_percentage'] = instance.discount_percentage()
        representation['stock_status'] = instance.stock_status()
        return representation
