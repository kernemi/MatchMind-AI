"""
Views for Jobs app
"""
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Job
from .serializers import JobSerializer, JobListSerializer


class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing job postings.
    Supports list, create, retrieve, update, partial_update, destroy.

    Filtering:
      ?status=applied         — filter by application status
      ?search=google          — search title or company
      ?ordering=-created_at   — sort (default: newest first)
    """
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'company', 'description']
    ordering_fields = ['created_at', 'updated_at', 'title', 'company', 'status']
    ordering = ['-created_at']

    def get_queryset(self):
        """Return only the current user's jobs, with optional status filter"""
        qs = Job.objects.filter(user=self.request.user)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)

        return qs

    def get_serializer_class(self):
        """Use lightweight serializer for list, full for everything else"""
        if self.action == 'list':
            return JobListSerializer
        return JobSerializer

    def perform_create(self, serializer):
        """Attach the current user when creating a job"""
        serializer.save(user=self.request.user)
