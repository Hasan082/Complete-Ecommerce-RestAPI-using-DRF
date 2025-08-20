from decimal import Decimal
from django.db import models
from django.conf import settings
from common.helper_models import TimeStampedModel
from products.models import Product
from user_accounts.models  import CustomUser


class Cart(TimeStampedModel):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="carts"
    )

    session_key = models.CharField(max_length=50, null=True, blank=True)


    class Meta(TimeStampedModel.Meta):
        constraints = [
            models.CheckConstraint(
                check=models.Q(user__isnull=True) | models.Q(session_key__isnull=True),
                name="user_or_session_key_required",
            ),
            models.UniqueConstraint(
                fields=["user"],
                name="unique_user_name",
                condition=models.Q(user__isnull=False),
            ),
            models.UniqueConstraint(
                fields=["session_key"],
                name="unique_session_key",
                condition=models.Q(session_key__isnull=False),
            ),
        ]

    def __str__(self):
        """
        Return a human-readable string representation of the cart.

        If the cart is associated with a user, it returns "Cart of <full name or email>".
        Otherwise, it returns "Cart of Anonymous".
        """
        if self.user:
            full_name = f"{self.user.first_name} {self.user.last_name}".strip()
            return f"Cart of {full_name or self.user.email}"
        return "Cart of Anonymous"
    
    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def total_items(self):
        return self.items.aggregate(total=models.Sum("quantity"))["total"] or 0  # type: ignore

    @property
    def subtotal(self):
        return sum(item.item_total for item in self.items.select_related("product"))  # type: ignore

    @property
    def total_discount(self):
        return sum(
            (item.product.price - item.product.discounted_price) * item.quantity
            for item in self.items.select_related("product") # type: ignore
        )

    @property
    def total(self):
        return self.subtotal

    def assign_to_user(self, user):
        self.user = user
        self.session_key = None
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    creaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")

    @property
    def item_total(self):
        """Total Price for this Cart Item"""
        return (self.product.discounted_price or self.product.price) * self.quantity
