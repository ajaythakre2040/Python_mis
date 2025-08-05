from rest_framework import serializers
from users.models.user import TblUser
from users.serializers.user_SessionSerializer import TblSessionSerializer
from django.contrib.auth.hashers import make_password
import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError as DjangoValidationError


class TblUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=False, 
        error_messages={
            "min_length": "Password must be at least 8 characters long.",
            "blank": "Password cannot be blank.",
        },
    )
    created_by = serializers.CharField(read_only=True)
    updated_by = serializers.CharField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    deleted_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = TblUser
        fields = [
            "id",
            "fullname",
            "mobileno",
            "email",
            "address",
            "gstno",
            "password",
            "is_active",
            "created_by",
            "updated_by",
            "updated_at",
            "deleted_at",
        ]

    def validate(self, data):
       
        if self.instance is None and "password" not in data:
            raise serializers.ValidationError({"password": "This field is required."})

       
        password = data.get("password")
        if password:
            errors = []
            if not re.search(r"[A-Z]", password):
                errors.append("an uppercase letter")
            if not re.search(r"[a-z]", password):
                errors.append("a lowercase letter")
            if not re.search(r"[0-9]", password):
                errors.append("a digit")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                errors.append("a special character")

            if errors:
                raise serializers.ValidationError(
                    {"password": f"Password must contain at least {', '.join(errors)}."}
                )

        return data

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        user_id = self.instance.id if self.instance else None
        if TblUser.objects.filter(email=value).exclude(id=user_id).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate_mobileno(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise serializers.ValidationError(
                "Mobile number must be exactly 10 digits."
            )
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["created_by"] = str(request.user.id)
        return TblUser.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Hash password if provided, otherwise do not update password
        password = validated_data.get("password")
        if password:
            validated_data["password"] = make_password(password)
        else:
            validated_data.pop(
                "password", None
            )  # Remove to avoid overwriting with None

        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["updated_by"] = str(request.user.id)

        return super().update(instance, validated_data)


class TblUserWithSessionsSerializer(serializers.ModelSerializer):
    sessions = serializers.SerializerMethodField()

    class Meta:
        model = TblUser
        fields = [
            "id",
            "fullname",
            "mobileno",
            "email",
            "address",
            "gstno",
            "is_active",
            "created_by",
            "updated_by",
            "updated_at",
            "deleted_at",
            "sessions",
        ]

    def get_sessions(self, obj):
        sessions = obj.sessions.filter(deleted_at__isnull=True)
        return TblSessionSerializer(sessions, many=True).data
