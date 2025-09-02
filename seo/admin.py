from django.contrib import admin
from .models import RedirectRule


@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = ['old_path', 'new_path', 'redirect_type', 'is_active', 'created_at']
    list_filter = ['redirect_type', 'is_active', 'created_at']
    search_fields = ['old_path', 'new_path']
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Redirect Configuration', {
            'fields': ('old_path', 'new_path', 'redirect_type')
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )
