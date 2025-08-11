from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    
    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image_url = models.ImageField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})
    
    def discount_percentage(self):
        if self.discounted_price and self.price:
            discount_amount = self.price - self.discounted_price
            percentage = (discount_amount / self.price) * 100
            return round(percentage, 2) 
        return 0
    
    def stock_status(self):
        if self.stock > 0:
            return "In Stock"
        return "Out of Stock"
    
    def __str__(self):
        return self.name