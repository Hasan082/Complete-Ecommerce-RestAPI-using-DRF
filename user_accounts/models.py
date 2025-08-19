from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    phone = models.CharField(max_length=14, blank=True, null=True)

    # Present Address
    present_full_name = models.CharField(max_length=255, blank=True, null=True)
    present_street_address = models.CharField(max_length=255, blank=True, null=True)
    present_apartment = models.CharField(max_length=255, blank=True, null=True)
    present_city = models.CharField(max_length=100, blank=True, null=True)
    present_state = models.CharField(max_length=100, blank=True, null=True)
    present_postal_code = models.CharField(max_length=20, blank=True, null=True)
    present_country = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email}'s profile"

    def save(self, *args, **kwargs):
        # Auto-fill full name if not set and user has first/last name
        if not self.present_full_name:
            full_name = self.user.get_full_name()  # combines first_name + last_name
            if full_name:
                self.present_full_name = full_name
        super().save(*args, **kwargs)
