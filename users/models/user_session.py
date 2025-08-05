from django.db import models
from .user import TblUser
import uuid
from django.utils import timezone  # Import for default timestamp if needed


class TblSession(models.Model):
    user = models.ForeignKey(TblUser, on_delete=models.CASCADE, related_name="sessions")
    key = models.CharField(max_length=255, unique=True)
    joining_date = models.DateField()
    expiry_date = models.DateField()
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)  # <-- Add this field

    def __str__(self):
        return f"Session for User ID {self.user.id} - Key: {self.key[:10]}..."

    class Meta:
        db_table = "tbl_user_session"
        verbose_name = "Session"
        verbose_name_plural = "Sessions"
