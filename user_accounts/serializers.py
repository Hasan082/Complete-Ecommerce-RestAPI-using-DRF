from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Profile
from django.db import models # Added for get_or_create to work with the manager

class CustomRegistrationSerializer(RegisterSerializer):
    _has_phone_field = False
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    def get_cleaned_data(self):
        """Returns validated registration data for user and profile."""
        # Use super() to get the base user data
        data = super().get_cleaned_data()
        
        # Add the extra fields to the data dictionary
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['phone'] = self.validated_data.get('phone', '')
        data['address'] = self.validated_data.get('address', '')
        
        return data
    
    def save(self, request):
        """Create user and their profile with extra fields."""
        # This will create the User instance
        user = super().save(request)
        
        # Get cleaned data from get_cleaned_data method
        cleaned_data = self.get_cleaned_data()
        
        # Save first_name and last_name directly to the user instance
        user.first_name = cleaned_data['first_name']
        user.last_name = cleaned_data['last_name']
        user.save()
        
        # Use get_or_create to handle the profile creation
        # It's an atomic operation and handles race conditions
        profile, created = Profile.objects.get_or_create(user=user)
        
        # Assign values to the profile instance
        profile.phone = cleaned_data['phone']
        profile.address = cleaned_data['address']
        
        # Save the profile once
        profile.save()
        
        return user