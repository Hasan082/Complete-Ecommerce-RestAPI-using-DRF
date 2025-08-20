from django.conf import settings
from django.db import models
from products.models import Product
from decimal import Decimal
from common.helper_models import Address


class ShippingAddress(Address):
    pass


class BillingAddress(Address):
    pass


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    shipping_address = models.OneToOneField(
        ShippingAddress, on_delete=models.CASCADE, related_name="order"
    )
    billing_address = models.OneToOneField(
        BillingAddress, on_delete=models.CASCADE, related_name="order"
    )
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return a human-readable string representation of the order.

        The string is in the format "Order <order_number> by <user>".
        """
        return f"Order {self.order_number} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot

    @property
    def total_price(self):
        """
        Total price of this OrderItem, calculated as the product of the quantity and
        the price of the item at the time of order creation.

        Returns:
            Decimal: The total price of the item.
        """
        return self.quantity * self.price

    def __str__(self):
        """
        Return a string representation of this OrderItem.

        Returns:
            str: A string in the format "N × Product Name", where N is the quantity of the item and
            Product Name is the title of the product.
        """
        product_name = self.product.title if self.product else "Unknown product"
        return f"{self.quantity} × {product_name}"
