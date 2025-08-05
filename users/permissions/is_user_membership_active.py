from rest_framework.permissions import BasePermission
from users.models.user_session import TblSession
from django.utils import timezone


class IsUserMembershipActive(BasePermission):
    """
    Allows access only if the user's most recent session (joining to expiry) is active.
    """

    message = "Your membership session is inactive or has expired."

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            self.message = "Authentication credentials are missing or invalid."
            return False

        # Get the latest active session by ID
        session = (
            TblSession.objects.filter(userid=user, is_active=True)
            .order_by("-id")
            .first()
        )

        if not session:
            self.message = "No active membership session found."
            return False

        today = timezone.now().date()

        if today < session.joining_date:
            self.message = "Your membership has not started yet."
            return False

        if today > session.expiry_date:
            self.message = "Your membership has expired. Please renew to continue."
            return False

        return True
