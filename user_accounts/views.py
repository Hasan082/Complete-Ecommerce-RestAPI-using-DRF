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
        """
        GET request handler for user details viewset.

        This method is overridden to merge the guest cart into the user's cart
        when the user logs in and views their account details.

        :param request: The current request object
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: The response object
        """
        merge_carts_on_login(request, request.user)
        return super().get(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        """
        PUT request handler for user details viewset.

        This method is overridden to merge the guest cart into the user's cart
        when the user updates their account details.

        :param request: The current request object
        :param args: Additional positional arguments
        :param kwargs: Additional keyword arguments
        :return: The response object
        """
        merge_carts_on_login(request, request.user)
        return super().put(request, *args, **kwargs)    # type: ignore


