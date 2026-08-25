"""
Admin configuration for Resumes app
"""
from django.contrib import admin
from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    """Resume admin"""
    list_display = ('name', 'user', 'file_size_kb', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('name', 'user__email')
    readonly_fields = ('uploaded_at', 'updated_at', 'file_size', 'extracted_text')
    ordering = ('-uploaded_at',)
    
    def file_size_kb(self, obj):
        """Display file size in KB"""
        return f"{obj.file_size / 1024:.2f} KB"
    file_size_kb.short_description = 'File Size'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'name', 'file', 'file_size')
        }),
        ('Extracted Data', {
            'fields': ('extracted_text', 'extracted_skills'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('uploaded_at', 'updated_at')
        }),
    )
