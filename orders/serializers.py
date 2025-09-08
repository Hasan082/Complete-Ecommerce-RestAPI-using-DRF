from rest_framework import serializers
from common.helper_serializers import BaseAddressSerializer
from .models import ShippingAddress, BillingAddress
from orders.models import Order, OrderItem


class ShippingAddressSerializer(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        model = ShippingAddress
        fields = [
            "full_name",
            "street_address",
            "apartment",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
        ]


class BillingAddressSerializer(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        model = BillingAddress
        fields = [
            "full_name",
            "street_address",
            "apartment",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
        ]


# --- Order Item ---
class OrderItemSerializers(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "product_title",
            "quantity",
            "price",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.total_price


# --- Order ---
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True)
    shipping_address = ShippingAddressSerializer()
    billing_address = BillingAddressSerializer()

    class Meta:
        model = Order
        fields = [
            "items",
            "order_number",
            "status",
            "total_amount",
            "shipping_address",
            "billing_address",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        shipping_data = validated_data.pop("shipping_address")
        billing_data = validated_data.pop("billing_address")

        # Create addresses
        shipping = ShippingAddress.objects.create(**shipping_data)
        billing = BillingAddress.objects.create(**billing_data)

        # Create order
        order = Order.objects.create(
            shipping_address=shipping, billing_address=billing, **validated_data
        )

        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
