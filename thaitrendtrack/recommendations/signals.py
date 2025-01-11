# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from .models import UserProfile
#
#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # Automatically create a UserProfile when a User is created
#         UserProfile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # Save the UserProfile whenever the User is saved
#     try:
#         instance.userprofile.save()
#     except UserProfile.DoesNotExist:
#         # Handle the case where the user doesn't have a profile
#         pass

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        # สร้าง UserProfile พร้อมค่าเริ่มต้น
        UserProfile.objects.create(
            user=instance,
            preferences=[],  # หรือใส่ค่าเริ่มต้นที่คุณต้องการ
            history=[]
        )

