from rest_framework import viewsets, parsers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer, ResumeListSerializer

class ResumeViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing resumes.
    Provides list, create, retrieve, update, and destroy actions.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_queryset(self):
        """Filter resumes to only those owned by the current user"""
        return Resume.objects.filter(user=self.request.user).order_by('-uploaded_at')

    def get_serializer_class(self):
        """Use list serializer for listing, detailed for everything else"""
        if self.action == 'list':
            return ResumeListSerializer
        return ResumeSerializer

    def perform_create(self, serializer):
        """Set the user when creating a new resume"""
        serializer.save(user=self.request.user)
