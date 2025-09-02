from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Brand, ProductCategory
import json


# Temporary simple serializers (we'll create proper ones next)
class ProductSerializer:
    def __init__(self, instance, many=False):
        self.instance = instance
        self.many = many
    
    @property
    def data(self):
        if self.many:
            return [self._serialize_product(item) for item in self.instance]
        return self._serialize_product(self.instance)
    
    def _serialize_product(self, product):
        return {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'brand': product.brand.name,
            'category': product.category.name,
            'slug': product.slug,
            'is_featured': product.is_featured,
        }


class BrandSerializer:
    def __init__(self, instance, many=False):
        self.instance = instance
        self.many = many
    
    @property
    def data(self):
        if self.many:
            return [self._serialize_brand(item) for item in self.instance]
        return self._serialize_brand(self.instance)
    
    def _serialize_brand(self, brand):
        return {
            'id': brand.id,
            'name': brand.name,
            'description': brand.description,
            'country_of_origin': brand.country_of_origin,
        }


class CategorySerializer:
    def __init__(self, instance, many=False):
        self.instance = instance
        self.many = many
    
    @property
    def data(self):
        if self.many:
            return [self._serialize_category(item) for item in self.instance]
        return self._serialize_category(self.instance)
    
    def _serialize_category(self, category):
        return {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'icon': category.icon,
        }


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for products"""
    queryset = Product.objects.filter(is_active=True).select_related('brand', 'category')
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand__name', 'category__name']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for brands"""
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'country_of_origin']
    ordering = ['name']


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API viewset for categories"""
    queryset = ProductCategory.objects.all()
    serializer_class = CategorySerializer
    ordering = ['name']


@api_view(['GET'])
def product_search(request):
    """Advanced product search API"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    brand = request.GET.get('brand', '')
    
    products = Product.objects.filter(is_active=True)
    
    if query:
        products = products.filter(
            models.Q(name__icontains=query) |
            models.Q(description__icontains=query) |
            models.Q(brand__name__icontains=query)
        )
    
    if category:
        products = products.filter(category__name__iexact=category)
    
    if brand:
        products = products.filter(brand__name__iexact=brand)
    
    products = products.select_related('brand', 'category')[:20]
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@csrf_exempt
def contact_form(request):
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            name = data.get('name', '')
            email = data.get('email', '')
            company = data.get('company', '')
            message = data.get('message', '')
            subject = data.get('subject', 'Website Contact Form')
            
            # Validate required fields
            if not all([name, email, message]):
                return JsonResponse({
                    'success': False,
                    'error': 'Please fill in all required fields.'
                }, status=400)
            
            # Compose email
            email_subject = f"[Sweet Bliss] {subject}"
            email_body = f"""
New contact form submission:

Name: {name}
Email: {email}
Company: {company}
Subject: {subject}

Message:
{message}

---
Sent from Sweet Bliss website contact form
            """
            
            # Send email
            send_mail(
                email_subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                ['azan@sweetbliss.pk'],  # Recipient email
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message. We will get back to you soon!'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'There was an error sending your message. Please try again.'
            }, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
