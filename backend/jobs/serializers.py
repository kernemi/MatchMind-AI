"""
Serializers for Jobs app
"""
from rest_framework import serializers
from .models import Job


class JobListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing jobs
    """
    analysis_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company', 'status',
            'url', 'created_at', 'updated_at', 'analysis_count'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'analysis_count')


class JobSerializer(serializers.ModelSerializer):
    """
    Full serializer for job create / retrieve / update
    """
    analysis_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = (
            'id', 'title', 'company', 'description',
            'url', 'status', 'notes', 'extracted_skills',
            'created_at', 'updated_at', 'analysis_count'
        )
        read_only_fields = ('id', 'extracted_skills', 'created_at', 'updated_at', 'analysis_count')

    def validate_url(self, value):
        """Allow empty URL, but validate format when provided"""
        if value and not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Enter a valid URL starting with http:// or https://")
        return value

    def validate_status(self, value):
        """Ensure status is one of the allowed choices"""
        valid = [c[0] for c in Job.STATUS_CHOICES]
        if value not in valid:
            raise serializers.ValidationError(f"Status must be one of: {', '.join(valid)}")
        return value
