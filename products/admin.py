from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug')
    search_fields = ('name',)
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    readonly_fields = ('discounted_price',)

