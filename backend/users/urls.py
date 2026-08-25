"""
URL patterns for Users app
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserProfileView
)

app_name = 'users'

urlpatterns = [
    # Registration and Login
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    
    # Token Refresh
    path('refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
]
