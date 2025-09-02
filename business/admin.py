from django.contrib import admin
from .models import TeamMember, ProductCategory, Brand, Product


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'email', 'is_active', 'order']
    list_filter = ['is_active', 'position']
    search_fields = ['name', 'position', 'email']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'name']


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name', 'description']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'country_of_origin', 'website_url']
    search_fields = ['name', 'country_of_origin']
    list_filter = ['country_of_origin']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'is_featured', 'is_active', 'created_at']
    list_filter = ['brand', 'category', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'brand__name']
    list_editable = ['is_featured', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'image')
        }),
        ('Classification', {
            'fields': ('category', 'brand')
        }),
        ('Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_featured', 'is_active')
        })
    )
