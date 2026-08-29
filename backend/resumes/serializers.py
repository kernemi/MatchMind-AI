import os
from rest_framework import serializers
from .models import Resume
from .pdf_processor import extract_text_from_pdf
from django.core.exceptions import ValidationError as DjangoValidationError

class ResumeListSerializer(serializers.ModelSerializer):
    """Serializer for listing resumes with minimal fields"""
    
    class Meta:
        model = Resume
        fields = ('id', 'name', 'file', 'file_size', 'uploaded_at', 'updated_at', 'analysis_count')
        read_only_fields = ('id', 'file', 'file_size', 'uploaded_at', 'updated_at', 'analysis_count')

class ResumeSerializer(serializers.ModelSerializer):
    """Detailed serializer for resume operations including upload"""
    
    class Meta:
        model = Resume
        fields = (
            'id', 'name', 'file', 'file_size', 
            'extracted_text', 'extracted_skills',
            'uploaded_at', 'updated_at', 'analysis_count'
        )
        read_only_fields = (
            'id', 'file_size', 'extracted_text', 
            'extracted_skills', 'uploaded_at', 'updated_at', 'analysis_count'
        )
        
    def validate_file(self, value):
        """Validate file size and type"""
        if not value:
            return value
            
        # 1. Validate file extension
        ext = os.path.splitext(value.name)[1].lower()
        if ext != '.pdf':
            raise serializers.ValidationError("Only PDF files are allowed.")
            
        # 2. Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if value.size > max_size:
            raise serializers.ValidationError("File size must be under 5MB.")
            
        return value

    def create(self, validated_data):
        """Extract text during creation"""
        file_obj = validated_data.get('file')
        
        # Set file size
        if file_obj:
            validated_data['file_size'] = file_obj.size
            
            # Extract text using PyMuPDF
            try:
                extracted_text = extract_text_from_pdf(file_obj)
                validated_data['extracted_text'] = extracted_text
            except DjangoValidationError as e:
                raise serializers.ValidationError({"file": list(e.messages)})
            
        return super().create(validated_data)
