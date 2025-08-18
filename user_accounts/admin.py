from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'address')

    def username(self, obj):
        return obj.user.username
    username.admin_order_field = 'user__username'  # type: ignore # allows sorting
    username.short_description = 'Username' # type: ignore

    def email(self, obj):
        return obj.user.email
    email.admin_order_field = 'user__email' # type: ignore
    email.short_description = 'Email' # type: ignore
    
    