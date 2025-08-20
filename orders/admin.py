from django.contrib import admin

from orders.models import Order, OrderItem

# Register your models here.
# admin.site.register(Order)
# admin.site.register(OrderItem)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "order_number",
        "status",
        "total_amount",
        "created_at",
        "updated_at",
    )

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = [
        "product",
        "order",
        "quantity",
        "price",
    ]
    list_display_links = [
        "product",
        "order",
    ]