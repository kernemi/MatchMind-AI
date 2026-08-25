"""
Job models for MatchMind AI
"""
from django.db import models
from django.conf import settings


class Job(models.Model):
    """
    Job model for storing job descriptions and tracking applications
    """
    
    STATUS_CHOICES = [
        ('saved', 'Saved'),
        ('applied', 'Applied'),
        ('interviewing', 'Interviewing'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='jobs',
        verbose_name='User'
    )
    title = models.CharField(max_length=255, verbose_name='Job Title')
    company = models.CharField(max_length=255, verbose_name='Company')
    description = models.TextField(verbose_name='Job Description')
    url = models.URLField(blank=True, max_length=500, verbose_name='Job URL')
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='saved',
        verbose_name='Application Status'
    )
    notes = models.TextField(blank=True, verbose_name='Notes')
    
    # Extracted data
    extracted_skills = models.JSONField(default=list, blank=True, verbose_name='Extracted Skills')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} at {self.company}"
    
    @property
    def analysis_count(self):
        """Return number of analyses for this job"""
        return self.analyses.count()
