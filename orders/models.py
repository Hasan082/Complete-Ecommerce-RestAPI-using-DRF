from django.conf import settings
from django.db import models
from products.models import Product
from decimal import Decimal


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
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shipping snapshot
    shipping_full_name = models.CharField(max_length=255)
    shipping_street_address = models.CharField(max_length=255)
    shipping_apartment = models.CharField(max_length=255, blank=True, null=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100, blank=True, null=True)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)
    shipping_phone = models.CharField(max_length=20, blank=True, null=True)

    # Billing snapshot
    billing_full_name = models.CharField(max_length=255)
    billing_street_address = models.CharField(max_length=255)
    billing_apartment = models.CharField(max_length=255, blank=True, null=True)
    billing_city = models.CharField(max_length=100)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_postal_code = models.CharField(max_length=20)
    billing_country = models.CharField(max_length=100)
    billing_phone = models.CharField(max_length=20, blank=True, null=True)

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
