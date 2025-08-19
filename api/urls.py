from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from products.views import CategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from rest_framework.routers import DefaultRouter
from user_accounts.views import UserDetailsViewSet
from dj_rest_auth.views import PasswordResetConfirmView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"cart", CartViewSet, basename="cart")


urlpatterns = [
    # Customer / Auth Endpoints
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('user/', UserDetailsViewSet.as_view(), name='custom_user_details'),
    # DJ REST API URLs
    path("", include("dj_rest_auth.urls")),
    path("registration/", include("dj_rest_auth.registration.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
] + router.urls
