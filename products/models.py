from decimal import Decimal
from typing import Iterable
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from autoslug import AutoSlugField
from django.core.exceptions import ValidationError
from common.helper_models import TimeStampedModel

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from="name", unique=True, db_index=True)  # type: ignore

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        """
        Return the absolute URL for this Category's detail page.

        Returns:
            str: The URL of this Category's detail page.
        """
        return reverse("category_detail", kwargs={"slug": self.slug})

    def __str__(self):
        """
        Return a string representation of the Category.

        Returns:
            str: The name of the Category.
        """
        return self.name


class Product(TimeStampedModel):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from="title", unique=True, db_index=True)  # type: ignore
    description = models.TextField(blank=True)
    image_url = models.ImageField(blank=True, upload_to="products")
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

    
    class Meta(TimeStampedModel.Meta):
        ordering = ["-created_at"]
        
    def clean(self):
        super().clean()
        if Product.objects.filter(title=self.title, categgory=self.category).exclude(pk=self.pk).exists():
            raise ValidationError("A product with this title already exists in this category.")
        if self.price <= 0:
            raise ValidationError("Price must be greater than zero.")
        # Validate discount percentage range
        if self.discount_percentage < 0 or self.discount_percentage > 100:
            raise ValidationError("Discount percentage must be between 0 and 100.")
        
    def save(self, *args, **kwargs):                        
        """
        Saves the product instance to the database.

        The method first calls `full_clean()` (Must call here before save data) to validate the data before saving.
        It then calculates the discounted price based on the price and discount
        percentage. The calculated discounted price is rounded to 2 decimal places.
        Finally, the method calls the parent class's `save()` method to save the
        product instance to the database. 
        """
        self.full_clean() 
        # Calculate discounted price from price and discount_percentage
        if self.discount_percentage>0:
            discount_amount = (self.price * self.discount_percentage) / 100
            self.discounted_price = round(self.price - discount_amount, 2)
        else:
            self.discounted_price = self.price
            
        super().save(*args, **kwargs)
        
        
    def get_absolute_url(self):
        """
        Returns the absolute URL for this product's detail page.
        """
        return reverse("product_detail", kwargs={"slug": self.slug})

    def stock_status(self):
        """
        Returns the stock status of the product as a string.
        Returns "In Stock" if the stock is greater than zero, otherwise "Out of Stock".
        """
        return "In Stock" if self.stock > 0 else "Out of Stock"

    def __str__(self):
        """
        Return a string representation of the product.

        Returns:
            str: The title of the product.
        """
        return self.title
