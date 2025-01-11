from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", verbose_name=_("User"))
    preferences = models.JSONField(default=list, blank=True, verbose_name=_("Preferences"))  # เก็บ genre ที่ชอบ
    history = models.JSONField(default=list, blank=True, verbose_name=_("Watch History"))  # เก็บประวัติหนังที่ดู
    is_first_login = models.BooleanField(default=True, verbose_name=_("Is First Login"))  # ตรวจสอบล็อกอินครั้งแรก

    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")
        ordering = ["user__username"]  # เรียงตามชื่อผู้ใช้งานเพื่อความชัดเจน

    def __str__(self):
        return self.user.username
