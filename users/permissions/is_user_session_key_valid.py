from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.utils.translation import gettext_lazy as _
from datetime import date
from users.models.user_session import TblSession


class SessionKeyAuthentication(BaseAuthentication):
    header_name = "Session-Key"

    def authenticate(self, request):
        session_key = request.headers.get(self.header_name)

        if not session_key:
            raise exceptions.AuthenticationFailed(_("Authentication key  is required."))

        session = self._get_valid_session(session_key)

        if not session.user:
            raise exceptions.AuthenticationFailed(_("Authentication  is not allow "))

        if not session.user.is_active:
            raise exceptions.AuthenticationFailed(_("User account is inactive."))

        return (session.user, session)

    def _get_valid_session(self, session_key):
        try:
            session = TblSession.objects.select_related("user").get(key=session_key)
        except TblSession.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                _("Api Authentication key is invalid.")
            )

        if session.user is None:
            raise exceptions.AuthenticationFailed(_("Authentication  is not allow."))

        if session.expiry_date < date.today():
            session.is_active = False
            session.save(update_fields=["is_active"])
            raise exceptions.AuthenticationFailed(_("Api Authentication has expired."))

        if not session.is_active:
            raise exceptions.AuthenticationFailed(_("Api Authentication is inactive."))

        return session
