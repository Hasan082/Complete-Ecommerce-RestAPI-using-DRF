from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(pre_save, sender=Order)
def generate_order_number(sender, instance, **kwargs):
    """
    Generate an order number for the Order instance if not already set.
    Format: ORD-XXXX
    """
    if not instance.order_number:
        last_order = Order.objects.all().order_by("-id").first()
        if last_order and last_order.order_number:
            try:
                last_order_number = int(last_order.order_number.split("-")[-1])
            except ValueError:
                last_order_number = 0
            new_order_number = last_order_number + 1
        else:
            new_order_number = 1

        instance.order_number = f"ORD-{new_order_number:04d}"


def update_order_total(order):
    """
    Sum total_price of all OrderItems and update order.total_amount
    """
    total = sum(item.total_price for item in order.items.all())
    order.total_amount = total
    order.save(update_fields=["total_amount"])


@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    """
    Update order total when an OrderItem is saved.
    """
    update_order_total(instance.order)


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    Update order total when an OrderItem is deleted.
    """
    update_order_total(instance.order)

