"""
Pytest configuration and shared fixtures
"""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Provide an API client for tests"""
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, django_user_model):
    """Provide an authenticated API client"""
    def _authenticated_client(user=None):
        if user is None:
            user = django_user_model.objects.create_user(
                email='test@example.com',
                password='TestPass123!',
                first_name='Test',
                last_name='User'
            )
        
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client, user
    
    return _authenticated_client
