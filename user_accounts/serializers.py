from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

# class CustomRegistrationSerializer(RegisterSerializer):
#     _has_phone_field = False  # Your own flag to track if phone is used
#     # phone_number = serializers.Char
    
#     def get_cleaned_data(self):
#         """Return validated registration data without forcing phone_number."""
#         data = super().get_cleaned_data()
        
#         return data
    
    
class CustomRegistrationSerializer(RegisterSerializer):
    _has_phone_field = True
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)

    def get_cleaned_data(self):
        """Return validated registration data including our required fields."""
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        data['phone_number'] = self.validated_data.get('phone_number', '')
        return data
