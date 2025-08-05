from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from datetime import timedelta
from user_agents import parse
from users.models.user import TblUser
from users.models.login_session import LoginSession
from users.serializers.reset_passwordSerializer import ResetPasswordSerializer
from users.serializers.userSerializer import TblUserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.conf import settings
from users.permissions.session_active import IsSessionActive  


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TblUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {"message": "Registration failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("username")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"message": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = TblUser.objects.get(email=email, is_active=True)
        except TblUser.DoesNotExist:
            return Response(
                {"message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not check_password(password, user.password):
            return Response(
                {"message": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        ip_address = request.data.get("ip_address")
        if not ip_address:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(",")[0].strip()
            else:
                ip_address = request.META.get("REMOTE_ADDR")

        agent_browser = request.data.get("agent_browser")
        if not agent_browser:
            user_agent_string = request.META.get("HTTP_USER_AGENT", "")
            user_agent = parse(user_agent_string)
            agent_browser = (
                f"{user_agent.browser.family} {user_agent.browser.version_string}"
            )

        expiry = timezone.now() + timedelta(days=settings.JWT_REFRESH_EXPIRY_DAYS)

        def get_tokens_for_user(user):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

        tokens = get_tokens_for_user(user)

        session = LoginSession.objects.create(
            user=user,
            expiry_at=expiry,
            login_at=timezone.now(),
            is_active=True,
            ip_address=ip_address,
            agent_browser=agent_browser,
            token=tokens["access"],
        )

        return Response(
            {
                "message": "Login successful.",
                "access_token": tokens["access"],
                "refresh_token": tokens["refresh"],
            },
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def post(self, request):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successfully."}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Password reset failed.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def post(self, request):
        user = request.user
        access_token = request.auth

        try:
            session = LoginSession.objects.get(
                user=user, token=access_token, is_active=True
            )
        except LoginSession.DoesNotExist:
            session = None

        ip_address = request.data.get("ip_address")
        if not ip_address:
            x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
            ip_address = (
                x_forwarded_for.split(",")[0].strip()
                if x_forwarded_for
                else request.META.get("REMOTE_ADDR")
            )

        agent_browser = request.data.get("agent_browser")
        if not agent_browser:
            user_agent_string = request.META.get("HTTP_USER_AGENT", "")
            user_agent = parse(user_agent_string)
            agent_browser = (
                f"{user_agent.browser.family} {user_agent.browser.version_string}"
            )

        if session:
            session.logout_at = timezone.now()
            session.is_active = False
            session.ip_address = ip_address
            session.agent_browser = agent_browser
            session.save()

        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"message": "Refresh token required for logout."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"message": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)
