from django.db import models
from django.conf import settings  # Use this to stay flexible with custom user models


class SessionKeyUsageLog(models.Model):
    session_key = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    endpoint = models.CharField(max_length=255)
    used_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    STATUS_CHOICES = [("success", "Success"), ("failed", "Failed")]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="success")

    def __str__(self):
        return f"{self.session_key} | {self.endpoint} | {self.status} | {self.used_at}"

    class Meta:
      db_table = "tbl_session_key_usage_log"

