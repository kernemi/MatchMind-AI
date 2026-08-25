"""
Admin configuration for Analysis app
"""
from django.contrib import admin
from .models import Analysis


@admin.register(Analysis)
class AnalysisAdmin(admin.ModelAdmin):
    """Analysis admin"""
    list_display = ('id', 'user', 'resume_name', 'job_title', 'match_score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'resume__name', 'job__title')
    readonly_fields = ('created_at', 'match_score', 'semantic_similarity')
    ordering = ('-created_at',)
    
    def resume_name(self, obj):
        return obj.resume.name
    resume_name.short_description = 'Resume'
    
    def job_title(self, obj):
        return f"{obj.job.title} at {obj.job.company}"
    job_title.short_description = 'Job'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('user', 'resume', 'job')
        }),
        ('Scores', {
            'fields': ('match_score', 'semantic_similarity')
        }),
        ('Skills Analysis', {
            'fields': ('matching_skills', 'missing_skills'),
            'classes': ('collapse',)
        }),
        ('Details', {
            'fields': ('keyword_analysis', 'suggestions'),
            'classes': ('collapse',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
