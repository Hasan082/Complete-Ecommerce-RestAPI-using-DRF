from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Profile

# class CustomRegistrationSerializer(RegisterSerializer):
#     _has_phone_field = False  # Your own flag to track if phone is used
#     # phone_number = serializers.Char
    
#     def get_cleaned_data(self):
#         """Return validated registration data without forcing phone_number."""
#         data = super().get_cleaned_data()
        
#         return data
    
    
class CustomRegistrationSerializer(RegisterSerializer):
    _has_phone_field = False
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    address = serializers.CharField(required=True)

    def get_cleaned_data(self):
        """Return validated registration data including our required fields."""
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['phone'] = self.validated_data.get('phone', '')
        data['address'] = self.validated_data.get('address', '')
        return data
    
    def save(self, request):
        """Create user and save extra fields to profile."""
        # Create the default user (username, email, password)
        user = super().save(request)
        
        # save the first name and last name to user
        user.first_name = self.validated_data.get("first_name", "")
        user.last_name = self.validated_data.get("last_name", "")
        user.save()
        
         # Save phone and address to the profile
        profile = getattr(user, 'profile', None)
        
        if profile is None:
            profile = Profile.objects.create(user=user)
             
        # Save phone and addresss to  user profile    
        profile.phone = self.validated_data.get("phone", "")
        profile.address = self.validated_data.get("address", "")
        profile.save()
        
        return user
