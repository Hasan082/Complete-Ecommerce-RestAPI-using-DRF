from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from products.views import CategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from user_accounts.views import CustomLoginView, CustomResendEmailView, CustomVerifyEmailView
from rest_framework.routers import DefaultRouter
from user_accounts.views import (
    CustomLoginView,
    CustomLogoutView,
    CustomPasswordChangeView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    CustomUserDetailsView,
    CustomRegisterView
)


router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"cart", CartViewSet, basename="cart")


urlpatterns = [
    # Customer / Auth Endpoints
    path('register/', CustomRegisterView.as_view(), name='custom_register'),
    path("register/resend-email/", CustomResendEmailView.as_view(), name="resend_email"),
    path("register/verify-email/", CustomVerifyEmailView.as_view(), name="verify_email"),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    path('logout/', CustomLogoutView.as_view(), name='custom_logout'),
    path('password/change/', CustomPasswordChangeView.as_view(), name='custom_password_change'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password/reset/confirm/', CustomPasswordResetConfirmView.as_view(), name='custom_password_reset_confirm'),
    path('profile/', CustomUserDetailsView.as_view(), name='custom_user_details'),
    # DJ REST API URLs
    # path("customer/", include("dj_rest_auth.urls")),
    # path("registration/", include("dj_rest_auth.registration.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + router.urls
