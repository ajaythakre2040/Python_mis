from django.db import models
from django.utils import timezone
from .user import TblUser
import uuid


class LoginSession(models.Model):
    user = models.ForeignKey(
        TblUser, on_delete=models.CASCADE, related_name="login_sessions"
    )
    token = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)
    login_at = models.DateTimeField(default=timezone.now)
    logout_at = models.DateTimeField(null=True, blank=True)
    expiry_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)
    agent_browser = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f"Session for {self.user.fullname} ({'active' if self.is_active else 'inactive'})"

    class Meta:
        db_table = "tbl_login_session"
        verbose_name = "Login Session"
        verbose_name_plural = "Login Sessions"
