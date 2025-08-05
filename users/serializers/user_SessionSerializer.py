from rest_framework import serializers
from users.models.user_session import TblSession


class TblSessionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.fullname", read_only=True)

    class Meta:
        model = TblSession
        fields = [
            "id",
            "user_id",
            "user_name",
            "key",
            "joining_date",
            "expiry_date",
            "is_active",
        ]
