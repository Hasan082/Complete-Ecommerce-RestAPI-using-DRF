# # user_accounts/adapter.py
# from allauth.account.adapter import DefaultAccountAdapter

# class CustomAccountAdapter(DefaultAccountAdapter):
#     def set_phone(self, user, phone):
#         # Save the phone to the related profile
#         profile = getattr(user, 'profile', None)
#         if profile is None:
#             from .models import Profile
#             profile = Profile.objects.create(user=user)
#         profile.phone = phone
#         profile.save()
