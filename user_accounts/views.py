from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import (
    UserDetailsView
)
from cart.utils import merge_carts_on_login
from user_accounts.serializers import UserSerializer, CustomRegistrationSerializer



@extend_schema(
    tags=["Profile"],
    summary="Profile endpoint summary",
    description="Profile Detailed description of what this API does.",
)
class UserDetailsViewSet(UserDetailsView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        merge_carts_on_login(request, request.user)
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        merge_carts_on_login(request, request.user)
        return super().put(request, *args, **kwargs)

