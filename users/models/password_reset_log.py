from django.db import models
from django.utils import timezone
from django.conf import settings


class UserPasswordResetLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_logs",
    )
    old_password_hash = models.CharField(max_length=255)
    new_password_hash = models.CharField(max_length=255)
    reset_at = models.DateTimeField(default=timezone.now)
    reset_by_user = models.BooleanField(default=True)  # False = admin-initiated

    class Meta:
        db_table = "tbl_reset_password"  # 👈 Custom DB table name
        ordering = ["-reset_at"]

    def __str__(self):
        return f"Password reset for {self.user.id} at {self.reset_at}"
