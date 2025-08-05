from users.models.SessionKeyUsageLog import SessionKeyUsageLog


def log_session_key_usage(request, endpoint: str, status: str = "success"):
    session_key = (
        request.headers.get("Session-Key")
        or request.query_params.get("sessionKey")
        or getattr(request.auth, "key", None)
    )
    user = request.user if request.user.is_authenticated else None
    ip_address = request.META.get("REMOTE_ADDR")

    if session_key and endpoint:
        SessionKeyUsageLog.objects.create(
            session_key=session_key,
            user=user,
            endpoint=endpoint,
            ip_address=ip_address,
            status=status,
        )