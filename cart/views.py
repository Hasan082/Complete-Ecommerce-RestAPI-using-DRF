from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.db.models import F

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
        """
        Retrieve current user's or guest's cart.
        
        Returns a CartSerializer representation of the cart.
        """
        cart = self._get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(summary="Add or update a cart item")
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        """
        Add or update a cart item.
        
        This endpoint receives a POST request with a JSON payload containing the
        product ID and quantity. It creates or updates a CartItem instance in the
        database with the given product and quantity. If an item with the same
        product ID already exists in the cart, it increases the quantity of the
        existing item by the given quantity. The response is a serialized CartItem
        instance with HTTP status 201 Created.
        """
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
        """
        Remove a cart item.

        This endpoint receives a POST request with a JSON payload containing the
        product ID. It deletes the CartItem instance from the database with the given
        product ID. If the deletion is successful, it returns a JSON response with
        {"removed": True}. If the deletion fails (because the item does not exist),
        it returns a JSON response with {"removed": False}.
        """
        cart = self._get_cart(request)
        product_id = request.data.get("product")
        deleted, _ = CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"removed": bool(deleted)})

    @extend_schema(summary="Clear all items in the cart")
    @action(detail=False, methods=["post"])
    def clear(self, request):
        """
        Clear all items in the cart.

        This endpoint receives a POST request. It deletes all CartItem instances
        associated with the current cart. If the deletion is successful, it returns
        a JSON response with {"status": "cart cleared"}.
        """
        cart = self._get_cart(request)
        cart.items.all().delete() # type: ignore
        return Response({"status": "cart cleared"})






