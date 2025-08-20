from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser, Profile


# -------------------------
# Registration Serializer
# -------------------------
class CustomRegistrationSerializer(RegisterSerializer):

    username = None  # No username
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)

    def get_cleaned_data(self):
        """Return validated registration data for user and profile."""
        data = super().get_cleaned_data()
        data.update(
            {
                "first_name": self.validated_data.get("first_name", ""),  # type: ignore
                "last_name": self.validated_data.get("last_name", ""),  # type: ignore
                "phone": self.validated_data.get("phone", ""),  # type: ignore
            }
        )
        return data

    def save(self, request):
        """Create user and their profile with extra fields."""
        user = super().save(request)
        cleaned_data = self.get_cleaned_data()

        user.first_name = cleaned_data["first_name"]
        user.last_name = cleaned_data["last_name"]
        user.save()

        # Ensure profile exists and set extra fields
        profile, created = Profile.objects.get_or_create(user=user)
        profile.phone = cleaned_data["phone"]
        profile.save()

        return user


# -------------------------
# Login Serializer
# -------------------------
class CustomLoginSerializer(LoginSerializer):
    username = None  # No username
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(self.context["request"], email=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid email or password")
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs["user"] = user
        return attrs


# -------------------------
# Profile Serializer
# -------------------------
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "phone",
            "present_full_name",
            "present_street_address",
            "present_apartment",
            "present_city",
            "present_state",
            "present_postal_code",
            "present_country",
        ]
        read_only_fields = [
            "present_full_name",
        ]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "profile",
        ]
        read_only_fields = ["is_active", "is_staff"]

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        if profile_data:
            profile, created = Profile.objects.get_or_create(user=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not instance.profile:
            ret["profile"] = {field: None for field in ProfileSerializer.Meta.fields}
        return ret
