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
    shipping_address = ShippingAddressSerializer()
    billing_address = BillingAddressSerializer()
    product_title = serializers.CharField(source="product.title", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "shipping_address",
            "billing_address",
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

    class Meta:
        model = Order
        fields = [
            "items",
            "order_number",
            "status",
            "total_amount",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            # Extract nested addresses
            shipping_data = item_data.pop("shipping_address", None)
            billing_data = item_data.pop("billing_address", None)

            # Get or create addresses to avoid duplicates
            shipping = None
            billing = None
            if shipping_data:
                shipping, _ = ShippingAddress.objects.get_or_create(**shipping_data)
            if billing_data:
                billing, _ = BillingAddress.objects.get_or_create(**billing_data)

            # Create order item
            OrderItem.objects.create(
                order=order,
                shipping_address=shipping,
                billing_address=billing,
                **item_data
            )

        return order
