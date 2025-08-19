from django.contrib import admin
from .models import Profile, CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import Group


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    model = CustomUser

    list_display = ("email","first_name", "last_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")

    fieldsets = (
        ("User Data", {"fields": ("email", "password", "first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'address')

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email' # type: ignore
    email.short_description = 'Email' # type: ignore
    
    def phone(self, obj):
        return obj.user.phone
    phone.admin_order_field = 'user__phone' # type: ignore
    phone.short_description = 'Phone' # type: ignore 
    
    def address(self, obj):
        return obj.user.address
    address.admin_order_field = 'user__address' # type: ignore
    address.short_description = 'Address' # type: ignore 
    
    