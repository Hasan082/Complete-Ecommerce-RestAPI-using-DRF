from dj_rest_auth.registration.serializers import RegisterSerializer


class CustomRegistrationSerializer(RegisterSerializer):
    _has_phone_field = False  # Your own flag to track if phone is used
    # phone_number = serializers.Char
    
    def get_cleaned_data(self):
        """Return validated registration data without forcing phone_number."""
        data = super().get_cleaned_data()
        
        return data
    
