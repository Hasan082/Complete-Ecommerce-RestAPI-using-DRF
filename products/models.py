from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from autoslug import AutoSlugField
from jsonschema import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True, db_index=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
        verbose_name = 'Category'
    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True, db_index=True)
    description = models.TextField(blank=True)
    image_url = models.ImageField(blank=True, null=True, upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Products'
        verbose_name = 'Product'

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    
    def clean(self):
        super().clean() 
        if self.discount_percentage < 0 or self.discount_percentage > 100:
            raise ValidationError(f"Percentage can not be less than 0 or more than 100")
        if self.discounted_price and self.price:
            if self.discounted_price >= self.price:
                raise ValidationError("Discounted price must be less than the original price")
            
    def save(self, *args, **kwargs):
        self.full_clean()
        
        self.discounted_price = (self.price - ((self.price * self.discount_percentage) / 100)) if self.discount_percentage > 0 else self.price

        super().save(*args, **kwargs)

    def stock_status(self):
        return "In Stock" if self.stock > 0 else "Out of Stock"
    
    def __str__(self):
        return self.title