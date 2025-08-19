from django.contrib import admin
from .models import Profile


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
    
    