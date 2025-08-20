from django.shortcuts import render
from rest_framework import viewsets
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializers
from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=["Order"],
    summary="Order endpoint summary",
    description="Order Detailed description of what this API does.",
)
class OrderViewwSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
@extend_schema(
    tags=["Order Items"],
    summary="Order Items endpoint summary",
    description="Order Items Detailed description of what this API does.",
)    
class OrderItemViewwSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderSerializer