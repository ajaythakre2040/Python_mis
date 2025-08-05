from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from users.models.login_session import LoginSession
from django.utils import timezone


class LoginSessionAuthentication(BaseAuthentication):
    """
    Custom authentication using Bearer <token> header.
    """

    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # No auth provided

        if not auth_header.startswith("Bearer "):
            return None  # Wrong prefix

        token = auth_header[7:].strip()  # Remove "Bearer " prefix

        if not token:
            raise AuthenticationFailed("No token provided.")

        try:
            session = LoginSession.objects.select_related("user").get(
                token=token, is_active=True
            )
        except LoginSession.DoesNotExist:
            raise AuthenticationFailed("Invalid or inactive token.")

        if session.expiry_at and session.expiry_at < timezone.now():
            session.is_active = False
            session.save()
            raise AuthenticationFailed("Token has expired.")

        return (session.user, session)
