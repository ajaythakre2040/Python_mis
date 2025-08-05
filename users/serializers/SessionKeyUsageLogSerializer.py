from rest_framework import serializers
from users.models import SessionKeyUsageLog 

class SessionKeyUsageLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.fullname", read_only=True)
    class Meta:
        model = SessionKeyUsageLog
        fields = [
            "id",
            # "session_key",
            "user",
            "user_name",
            "endpoint",
            "used_at",
            "ip_address",
            "status",
        ]
        read_only_fields = ["id", "used_at"]
