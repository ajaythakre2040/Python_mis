from rest_framework.permissions import BasePermission
from users.models.login_session import LoginSession  # Adjust import path as needed
from users.models.user_session import TblSession


class IsSessionActive(BasePermission):
    message = "Your session is invalid or has expired. Please log in again."

    def has_permission(self, request, view):
        user = request.user
        token = str(request.auth)  # Ensure token is a string

        if not user or not user.is_authenticated:
            self.message = (
                "Authentication credentials were not provided or are invalid."
            )
            return False

        try:
            latest_session = (
                LoginSession.objects.filter(user=user, is_active=True)
                .order_by("-id")
                .first()
            )

            if not latest_session:
                self.message = (
                    "No active session found for this user. Please authenticate again."
                )
                return False

            if str(latest_session.token) != token:
                self.message = "This token does not match your latest login session. Please re-authenticate."
                return False

            return True
        except Exception as e:
            self.message = "An error occurred while validating your session. Please try again later."
            return False
