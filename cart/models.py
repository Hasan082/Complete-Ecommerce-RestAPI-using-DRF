from decimal import Decimal
from django.db import models
from django.conf import settings
from products.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
    # Option user for anonymious carts
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    # Session key for guest users
    session_key = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            #Ensure either user or session_key exist
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(session_key__isnull=False),
                name = "user_or_session_key_required"
            ),
            # Each user have only one cart
            models.UniqueConstraint(fields=['user'], name='unique_user_name'),
            # Each session have only one cart
            models.UniqueConstraint(fields=['session_key'], name="unique_session_key"),
        ]
    
    
    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Anonymous Cart ({self.session_key})"
    
    @property
    def is_anonymous(self):
        return self.user is None
    
    @property
    def total_items(self):
        """Total Quantity of all the items in the cart"""
        return self.items.agregrate(total=models.Sum('quantity'))['total'] or 0 # type: ignore
    
    @property
    def subtotal(self):
        """Total price using discounted prices"""
        return sum(item.item_total for item in self.items.select_related('product').all()) # type: ignore
    
    @property
    def total_discount(self):
        """Total SAviong from discount"""
        return sum(
            (item.product.price - item.product.discounted_price) for item in self.items.select_related('product').all() # type: ignore
        )
        
    @property
    def total(self):
        """Total amount payable(can add tax or shipping later)"""
        return self.subtotal
    
    def assign_to_user(self, user):
        """Assign a guset cart to registered user"""
        self.user = user
        self.session_key = None
        self.save()
        
        
        
                
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items' ,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('cart', 'product')
        
    @property
    def item_total(self):
        """Total Price for this Cart Item"""
        return (self.product.discounted_price or self.product.price) * self.quantity