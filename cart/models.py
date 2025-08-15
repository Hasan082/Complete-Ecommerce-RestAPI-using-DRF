from decimal import Decimal
from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        items = self.items.all()
        total = sum([item.total_price for item in items])
        return total

    @property
    def total_items(self):
        return self.items.count()

    def __str__(self):
        return f"Cart ({self.user})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        # Use discounted_price if available
        price = self.product.discounted_price or self.product.price
        return price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
