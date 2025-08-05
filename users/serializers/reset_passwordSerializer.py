from rest_framework import serializers
import re
from django.contrib.auth.hashers import check_password, make_password
from users.models import UserPasswordResetLog


class ResetPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")
        user = self.context["request"].user

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {"confirm_password": "New password and confirm password do not match."}
            )

        if check_password(new_password, user.password):
            raise serializers.ValidationError(
                {"new_password": "New password cannot be the same as the old password."}
            )

        errors = []
        if not re.search(r"[A-Z]", new_password):
            errors.append("an uppercase letter")
        if not re.search(r"[a-z]", new_password):
            errors.append("a lowercase letter")
        if not re.search(r"[0-9]", new_password):
            errors.append("a digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
            errors.append("a special character")

        if errors:
            raise serializers.ValidationError(
                {"new_password": f"Password must contain at least {', '.join(errors)}."}
            )

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        old_password_hash = user.password
        new_password = self.validated_data["new_password"]

        user.password = make_password(new_password)
        user.save(update_fields=["password"])

        UserPasswordResetLog.objects.create(
            user=user,
            old_password_hash=old_password_hash,
            new_password_hash=user.password,
            reset_by_user=True,
        )

        return user
