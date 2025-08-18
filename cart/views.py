from rest_framework import generics, permissions
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer


# Fetch current user's cart (read-only)
class MyCartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): # type: ignore
        return Cart.objects.get(user=self.request.user)


# Add or update a cart item
class AddCartItemView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()


# Remove a cart item
class RemoveCartItemView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self): # type: ignore
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product_id = self.kwargs['product_id']
        return CartItem.objects.get(cart=cart, product_id=product_id)
