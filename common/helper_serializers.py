from rest_framework import serializers
from .helper_models import Address

class BaseAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "full_name",
            "street_address",
            "apartment",
            "city",
            "state",
            "postal_code",
            "country",
            "phone"
        ]
