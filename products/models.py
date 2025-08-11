from decimal import Decimal
from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from autoslug import AutoSlugField
from jsonschema import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, db_index=True)  # type: ignore

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True, db_index=True)  # type: ignore
    description = models.TextField(blank=True)
    image_url = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    stock = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Enter discount percent (0-100).",
    )
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, editable=False
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def clean(self):
        super().clean()
        # Validate discount percentage range
        if self.discount_percentage < 0 or self.discount_percentage > 100:
            raise ValidationError("Discount percentage must be between 0 and 100.")
        
    def save(self, *args, **kwargs):
        self.full_clean() # Must call here before save data
        # Calculate discounted price from price and discount_percentage
        if self.discount_percentage>0:
            discount_amount = (self.price * self.discount_percentage) / 100
            self.discounted_price = self.price - discount_amount
        else:
            self.discounted_price = self.price
            
        super().save(*args, **kwargs)
        
        
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def stock_status(self):
        return "In Stock" if self.stock > 0 else "Out of Stock"

    def __str__(self):
        return self.title
