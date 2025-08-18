from dj_rest_auth.views import LoginView
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from django.db.models import F
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ViewSet):
    """
    A viewset for CartViewSet:
    - One cart per user (or per session for guests).
    - Provides endpoints to get cart, add items, remove items, and clear cart.
    """

    permission_classes = [permissions.AllowAny]  # guest carts allowed

    def _get_cart(self, request):
        """Helper: fetch or create the current cart (user or guest)."""
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
        return cart

    @extend_schema(summary="Retrieve current user's or guest's cart")
    def list(self, request):
        cart = self._get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(summary="Add or update a cart item")
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart = self._get_cart(request)
        product = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity = F("quantity") + quantity
            cart_item.save(update_fields=["quantity"])

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(summary="Remove a cart item")
    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        cart = self._get_cart(request)
        product_id = request.data.get("product")
        deleted, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"removed": bool(deleted)})

    @extend_schema(summary="Clear all items in the cart")
    @action(detail=False, methods=["post"])
    def clear(self, request):
        cart = self._get_cart(request)
        cart.items.all().delete() # type: ignore
        return Response({"status": "cart cleared"})




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


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        # 1. Call the original dj-rest-auth LoginView's post method
        response = super().post(request, *args, **kwargs)
        
        # 2. Get the authenticated user from the request
        user = self.request.user

        # 3. Perform the cart merging logic
        if user.is_authenticated:
            merge_carts_on_login(request, user)

        return response