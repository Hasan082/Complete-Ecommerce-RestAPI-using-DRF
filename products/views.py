from django.shortcuts import render
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly




class CategryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    read_only_fields = ['slug']
    lookup_field = 'slug'
