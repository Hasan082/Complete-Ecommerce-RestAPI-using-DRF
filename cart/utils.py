from cart.models import Cart
from django.db.models import F

def merge_carts_on_login(request, user):
    """
    A helper function to handle the cart merging logic.
    """
    session_key = request.session.session_key
    if not session_key:
        return

    try:
        anonymous_cart = Cart.objects.get(session_key=session_key, user__isnull=True)
        user_cart, created = Cart.objects.get_or_create(user=user)

        if not created:
            for anonymous_item in anonymous_cart.items.all(): # type: ignore
                # Use update_or_create for efficiency
                user_cart.items.update_or_create( # type: ignore
                    product=anonymous_item.product,
                    defaults={'quantity': F('quantity') + anonymous_item.quantity},
                )
        else:
            anonymous_cart.assign_to_user(user)
        
        anonymous_cart.delete()

    except Cart.DoesNotExist:
        pass
