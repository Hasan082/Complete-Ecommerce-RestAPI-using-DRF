from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem


@receiver(pre_save, sender=Order)
def genrate_order_number(sender, instance, **kwargs):
    """
    Generate an order number for the given Order model instance.

    If the order_number is not already set, generate a new one by
    incrementing the order number of the last saved Order instance.
    The order number is in the format of "ORD-XXXX" where XXXX is
    the order number with leading zeros up to four digits.
    """
    if not instance.order_number:
        last_order = Order.objects.all().order_by("-id").first()
        if last_order and last_order.order_number:
            try:
                last_order_number = int(instance.order_number.split("-")[-1])
            except ValueError:
                last_order_number = 0
            new_order_number = last_order_number + 1
        else:
            new_order_number = 1
            
        instance.order_number = f"ORD-{new_order_number:04d}"


def update_order_total(order):
    """
    Update the total_amount field of an Order model instance
    by summing up the total_price of all related OrderItem model instances.
    """
    total = sum(item.total_price for item in order.items.all())
    order.total_amount = total
    order.save(update_fields=["total_amount"])


@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    """
    Signal receiver to update the total_amount of an Order model instance
    whenever an OrderItem model instance is saved (created or updated).
    """
    update_order_total(instance.order)


@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    Signal receiver to update the total_amount of an Order model instance
    whenever an OrderItem model instance is deleted.
    """
    update_order_total(instance.order)
