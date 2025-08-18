from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import CustomLoginSerializer, UserSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
    UserDetailsView,
    LogoutView,
)
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView,
    ResendEmailVerificationView,
)
from cart.utils import merge_carts_on_login


@extend_schema(tags=["Authentication"], summary="Register a new user")
class CustomRegisterView(RegisterView):
    http_method_names = ["post"]  # only allow POST


@extend_schema(tags=["Authentication"], summary="Log in the user")
class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    http_method_names = ["post"]  # only allow POST
    def post(self, request, *args, **kwargs):
        # 1. Call the original dj-rest-auth LoginView's post method
        """
        Log in the user and perform cart merging logic if the user is authenticated.

        This method is overridden from the dj-rest-auth LoginView.

        Args:
            request (HttpRequest): The request object sent to the server.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The response object containing the result of the request.
        """
        response = super().post(request, *args, **kwargs)

        # 2. Get the authenticated user from the request
        user = self.request.user

        # 3. Perform the cart merging logic
        if user.is_authenticated:
            merge_carts_on_login(request, user)

        return response


class LogoutSerializer(serializers.Serializer):
    detail = serializers.CharField(read_only=True)
    

@extend_schema(tags=["Authentication"], request=LogoutSerializer, responses=LogoutSerializer)
class CustomLogoutView(LogoutView):
    http_method_names = ["post"]
    pass


@extend_schema(tags=["Authentication"], summary="Change password")
class CustomPasswordChangeView(PasswordChangeView):
    http_method_names = ["post"]
    pass


@extend_schema(tags=["Authentication"], summary="Request password reset")
class CustomPasswordResetView(PasswordResetView):
    pass


@extend_schema(tags=["Authentication"], summary="Confirm password reset")
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass


@extend_schema(tags=["User Profile"], summary="Retrieve or update Authentication info")
class CustomUserDetailsView(UserDetailsView):
    pass


@extend_schema(tags=["Authentication"], summary="Resend verification email")
class CustomResendEmailView(ResendEmailVerificationView):
    pass


@extend_schema(tags=["Authentication"], summary="Verify email with key")
class CustomVerifyEmailView(VerifyEmailView):
    pass
