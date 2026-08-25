"""
Tests for Users app
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User


@pytest.fixture
def api_client():
    """API client fixture"""
    return APIClient()


@pytest.fixture
def test_user_data():
    """Test user data fixture"""
    return {
        'email': 'test@example.com',
        'password': 'TestPass123!',
        'password_confirm': 'TestPass123!',
        'first_name': 'Test',
        'last_name': 'User'
    }


@pytest.fixture
def create_user():
    """Fixture to create a test user"""
    def _create_user(**kwargs):
        defaults = {
            'email': 'user@example.com',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'TestPass123!'
        }
        defaults.update(kwargs)
        password = defaults.pop('password')
        user = User.objects.create_user(**defaults)
        user.set_password(password)
        user.save()
        return user
    return _create_user


@pytest.mark.django_db
class TestUserRegistration:
    """Test user registration"""
    
    def test_register_user_success(self, api_client, test_user_data):
        """Test successful user registration"""
        url = reverse('users:register')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == test_user_data['email'].lower()
        assert response.data['first_name'] == test_user_data['first_name']
        assert 'password' not in response.data
        
        # Verify user was created in database
        assert User.objects.filter(email=test_user_data['email'].lower()).exists()
    
    def test_register_user_password_mismatch(self, api_client, test_user_data):
        """Test registration fails when passwords don't match"""
        test_user_data['password_confirm'] = 'DifferentPass123!'
        url = reverse('users:register')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
    
    def test_register_user_duplicate_email(self, api_client, test_user_data, create_user):
        """Test registration fails with duplicate email"""
        create_user(email=test_user_data['email'])
        
        url = reverse('users:register')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
    
    def test_register_user_weak_password(self, api_client, test_user_data):
        """Test registration fails with weak password"""
        test_user_data['password'] = '123'
        test_user_data['password_confirm'] = '123'
        
        url = reverse('users:register')
        response = api_client.post(url, test_user_data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'password' in response.data
    
    def test_register_user_missing_fields(self, api_client):
        """Test registration fails with missing required fields"""
        url = reverse('users:register')
        response = api_client.post(url, {}, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data
        assert 'password' in response.data
        assert 'first_name' in response.data


@pytest.mark.django_db
class TestUserLogin:
    """Test user login"""
    
    def test_login_success(self, api_client, create_user):
        """Test successful login returns tokens"""
        user = create_user()
        
        url = reverse('users:login')
        response = api_client.post(url, {
            'email': user.email,
            'password': 'TestPass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data
        assert response.data['user']['email'] == user.email
    
    def test_login_invalid_credentials(self, api_client, create_user):
        """Test login fails with invalid credentials"""
        user = create_user()
        
        url = reverse('users:login')
        response = api_client.post(url, {
            'email': user.email,
            'password': 'WrongPassword123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_nonexistent_user(self, api_client):
        """Test login fails for nonexistent user"""
        url = reverse('users:login')
        response = api_client.post(url, {
            'email': 'nonexistent@example.com',
            'password': 'TestPass123!'
        }, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_login_missing_fields(self, api_client):
        """Test login fails with missing fields"""
        url = reverse('users:login')
        response = api_client.post(url, {'email': 'test@example.com'}, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestTokenRefresh:
    """Test token refresh"""
    
    def test_refresh_token_success(self, api_client, create_user):
        """Test successful token refresh"""
        user = create_user()
        
        # Login to get tokens
        login_url = reverse('users:login')
        login_response = api_client.post(login_url, {
            'email': user.email,
            'password': 'TestPass123!'
        }, format='json')
        
        refresh_token = login_response.data['refresh']
        
        # Refresh the token
        refresh_url = reverse('users:token-refresh')
        response = api_client.post(refresh_url, {
            'refresh': refresh_token
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
    
    def test_refresh_token_invalid(self, api_client):
        """Test refresh fails with invalid token"""
        refresh_url = reverse('users:token-refresh')
        response = api_client.post(refresh_url, {
            'refresh': 'invalid-token'
        }, format='json')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUserProfile:
    """Test user profile endpoints"""
    
    def test_get_profile_authenticated(self, api_client, create_user):
        """Test authenticated user can get their profile"""
        user = create_user()
        
        # Login to get token
        login_url = reverse('users:login')
        login_response = api_client.post(login_url, {
            'email': user.email,
            'password': 'TestPass123!'
        }, format='json')
        
        access_token = login_response.data['access']
        
        # Get profile
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('users:profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['email'] == user.email
        assert response.data['first_name'] == user.first_name
        assert 'resume_count' in response.data
        assert 'job_count' in response.data
        assert 'analysis_count' in response.data
    
    def test_get_profile_unauthenticated(self, api_client):
        """Test unauthenticated user cannot access profile"""
        profile_url = reverse('users:profile')
        response = api_client.get(profile_url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_profile_authenticated(self, api_client, create_user):
        """Test authenticated user can update their profile"""
        user = create_user()
        
        # Login to get token
        login_url = reverse('users:login')
        login_response = api_client.post(login_url, {
            'email': user.email,
            'password': 'TestPass123!'
        }, format='json')
        
        access_token = login_response.data['access']
        
        # Update profile
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('users:profile')
        response = api_client.patch(profile_url, {
            'first_name': 'Updated',
            'last_name': 'Name'
        }, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['first_name'] == 'Updated'
        assert response.data['last_name'] == 'Name'
        
        # Verify update in database
        user.refresh_from_db()
        assert user.first_name == 'Updated'
        assert user.last_name == 'Name'
    
    def test_cannot_update_email(self, api_client, create_user):
        """Test user cannot change their email via profile update"""
        user = create_user()
        original_email = user.email
        
        # Login to get token
        login_url = reverse('users:login')
        login_response = api_client.post(login_url, {
            'email': user.email,
            'password': 'TestPass123!'
        }, format='json')
        
        access_token = login_response.data['access']
        
        # Try to update email
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        profile_url = reverse('users:profile')
        response = api_client.patch(profile_url, {
            'email': 'newemail@example.com'
        }, format='json')
        
        # Email should remain unchanged
        user.refresh_from_db()
        assert user.email == original_email


@pytest.mark.django_db
class TestUserModel:
    """Test User model"""
    
    def test_create_user(self):
        """Test creating a user"""
        user = User.objects.create_user(
            email='test@example.com',
            password='TestPass123!',
            first_name='Test',
            last_name='User'
        )
        
        assert user.email == 'test@example.com'
        assert user.check_password('TestPass123!')
        assert user.is_active
        assert not user.is_staff
    
    def test_user_full_name(self):
        """Test user full_name property"""
        user = User(first_name='John', last_name='Doe')
        assert user.full_name == 'John Doe'
    
    def test_user_str(self):
        """Test user string representation"""
        user = User(email='test@example.com')
        assert str(user) == 'test@example.com'
