from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'business'

# REST API URLs
router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'brands', views.BrandViewSet)
router.register(r'categories', views.CategoryViewSet)

urlpatterns = [
    # API endpoints for AJAX functionality
    path('api/search/', views.product_search, name='product_search'),
    path('api/contact/', views.contact_form, name='contact_form'),
] + router.urls
