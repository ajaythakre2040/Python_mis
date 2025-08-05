from rest_framework import serializers
from users.models.login_session import LoginSession


class LoginSessionSerializer(serializers.ModelSerializer):
    user_fullname = serializers.CharField(source="user.fullname", read_only=True)

    class Meta:
        model = LoginSession
        fields = ["token", "created_at", "expiry_at", "is_active", "user_fullname"]
        read_only_fields = ["token", "created_at", "is_active", "user_fullname"]
