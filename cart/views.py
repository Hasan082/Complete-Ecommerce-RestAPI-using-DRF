from rest_framework import generics, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from drf_spectacular.utils import extend_schema

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


@extend_schema(tags=["Cart"])
class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(summary="Retrieve current user's cart")
    def retrieve(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @extend_schema(summary="Add or update a cart item")
    @action(detail=False, methods=["post"])
    def add_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = request.data.get("product")
        quantity = int(request.data.get("quantity", 1))
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product_id=product
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @extend_schema(summary="Remove a cart item")
    @action(detail=False, methods=["post"], url_path="remove_item")
    def remove_item(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get("product")
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        return Response({"status": "item removed"})
