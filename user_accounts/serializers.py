from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CustomRegistrationSerializer(RegisterSerializer):
    _has_phone_field = False

    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    def get_cleaned_data(self):
        """Returns validated registration data for user and profile."""
        # Use super() to get the base user data
        data = super().get_cleaned_data()
        
        data.update({
            'first_name': self.validated_data.get('first_name', ''), # type: ignore
            'last_name': self.validated_data.get('last_name', ''),  # type: ignore
            'phone': self.validated_data.get('phone', ''), # type: ignore
            'address': self.validated_data.get('address', ''), # type: ignore
        })
        
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
    

# class CustomLoginSerializer(LoginSerializer):
#     username = None
#     email = serializers.EmailField(required=True)
#     password = serializers.CharField(required=True, write_only=True)   
    

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']
        read_only_fields = ['id', 'username', 'email']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profile fields
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance
