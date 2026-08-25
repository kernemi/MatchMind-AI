"""
Analysis models for MatchMind AI
"""
from django.db import models
from django.conf import settings


class Analysis(models.Model):
    """
    Analysis model for storing resume-job compatibility analysis results
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='User'
    )
    resume = models.ForeignKey(
        'resumes.Resume',
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='Resume'
    )
    job = models.ForeignKey(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='analyses',
        verbose_name='Job'
    )
    
    # Analysis results
    match_score = models.FloatField(verbose_name='Overall Match Score (0-100)')
    semantic_similarity = models.FloatField(verbose_name='Semantic Similarity (0-1)')
    
    # Skill analysis
    matching_skills = models.JSONField(default=list, verbose_name='Matching Skills')
    missing_skills = models.JSONField(default=list, verbose_name='Missing Skills')
    
    # Keyword analysis
    keyword_analysis = models.JSONField(default=dict, verbose_name='Keyword Analysis')
    
    # Suggestions
    suggestions = models.JSONField(default=list, verbose_name='Improvement Suggestions')
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Analyzed At')
    
    class Meta:
        db_table = 'analyses'
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['resume', '-created_at']),
            models.Index(fields=['job', '-created_at']),
        ]
    
    def __str__(self):
        return f"Analysis {self.id}: {self.resume.name} vs {self.job.title} ({self.match_score}%)"
