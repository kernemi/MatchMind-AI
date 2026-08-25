"""
Resume models for MatchMind AI
"""
from django.db import models
from django.conf import settings


class Resume(models.Model):
    """
    Resume model for storing user's resume files and extracted data
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='User'
    )
    name = models.CharField(max_length=255, verbose_name='Resume Name')
    file = models.FileField(upload_to='resumes/%Y/%m/%d/', verbose_name='Resume File')
    file_size = models.IntegerField(default=0, verbose_name='File Size (bytes)')
    
    # Extracted data
    extracted_text = models.TextField(blank=True, verbose_name='Extracted Text')
    extracted_skills = models.JSONField(default=list, blank=True, verbose_name='Extracted Skills')
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated At')
    
    class Meta:
        db_table = 'resumes'
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', '-uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"
    
    @property
    def analysis_count(self):
        """Return number of analyses using this resume"""
        return self.analyses.count()
