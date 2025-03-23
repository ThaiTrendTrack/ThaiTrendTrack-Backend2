from django.contrib import admin
from .models import UserProfile
from .models import Community

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_first_login', 'preferences', 'history']
    search_fields = ['user__username']


admin.site.register(Community)
