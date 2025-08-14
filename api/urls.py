from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from products.views import CategoryViewSet, ProductViewSet



from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='products')



urlpatterns = [
    
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
