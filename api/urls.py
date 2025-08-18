from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from products.views import CategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from cart.views import CustomLoginView
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import LogoutView, UserDetailsView, PasswordResetView, PasswordResetConfirmView


router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'cart', CartViewSet, basename='cart')


urlpatterns = [
    # Use your custom login view
    path('customer/login/', CustomLoginView.as_view(), name='custom_login'),
    path('customer/logout/', LogoutView.as_view(), name='rest_logout'),
    path('customer/user/', UserDetailsView.as_view(), name='rest_user_details'),
    path('customer/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('customer/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    # Rest API URLs
    path('customer/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    )
] + router.urls
