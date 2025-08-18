from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import (
    UserDetailsView
)
from cart.utils import merge_carts_on_login


class UserDetailsViewSet(UserDetailsView):
    def get(self, request, *args, **kwargs):
        merge_carts_on_login(request, request.user)
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        merge_carts_on_login(request, request.user)
        return super().put(request, *args, **kwargs)    # type: ignore


