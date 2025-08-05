from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models
from django.utils import timezone


class TblUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class TblUser(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=100)
    mobileno = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    gstno = models.CharField(max_length=20, blank=True, null=True)

    # Required for AbstractBaseUser
    password = models.CharField(max_length=128)

    # Permissions-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Audit fields
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=100, blank=True, null=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = TblUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["fullname", "mobileno"]

    class Meta:
        db_table = "tbl_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.fullname
