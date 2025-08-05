from django.core.management.base import BaseCommand
from users.models.user import TblUser
from users.serializers import TblUserSerializer  # Adjust path based on your project
from django.utils import timezone


class Command(BaseCommand):
    help = "Seed an admin user into TblUser using TblUserSerializer"

    def handle(self, *args, **kwargs):
        admin_data = {
            "email": "admin@gmail.com",
            "password": "Admin@12345",
            "fullname": "Admin User",
            "mobileno": "9876543210",
            "address": "Admin Address",
            "gstno": "22AAAAA0000A1Z5",
            "is_active": True,
        }

        if TblUser.objects.filter(email=admin_data["email"]).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Admin user with email {admin_data['email']} already exists."
                )
            )
        else:
            serializer = TblUserSerializer(data=admin_data)
            if serializer.is_valid():
                serializer.save(
                    is_staff=True, is_superuser=True, created_at=timezone.now()
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Admin user created with email: {admin_data['email']} and password: {admin_data['password']}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.ERROR(
                        f"Failed to create admin user: {serializer.errors}"
                    )
                )
