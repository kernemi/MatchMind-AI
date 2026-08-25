"""
Admin configuration for Jobs app
"""
from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """Job admin"""
    list_display = ('title', 'company', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('title', 'company', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'title', 'company', 'description', 'url')
        }),
        ('Application Tracking', {
            'fields': ('status', 'notes')
        }),
        ('Extracted Data', {
            'fields': ('extracted_skills',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
