from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models.user_session import TblSession
from users.models.user import TblUser
from users.permissions.session_active import IsSessionActive
from users.serializers.user_SessionSerializer import TblSessionSerializer

from datetime import datetime
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.models.user import TblUser
from users.models.user_session import TblSession
from users.serializers.user_SessionSerializer import TblSessionSerializer
from datetime import datetime
from dateutil.relativedelta import relativedelta
import uuid
from rest_framework.permissions import IsAuthenticated, AllowAny


class UserSessionCreateView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def post(self, request):
        user_id = request.data.get("user_id")
        joining_date_str = request.data.get("joining_date")
        no_months = request.data.get("months")
        is_active = request.data.get("is_active", True)

        if not user_id or not joining_date_str or no_months is None:
            return Response(
                {"message": "user_id, joining_date, and months are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = TblUser.objects.get(
                id=user_id, is_active=True, deleted_at__isnull=True
            )
        except TblUser.DoesNotExist:
            return Response(
                {"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"message": "Invalid joining_date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            no_months = int(no_months)
            if no_months <= 0:
                raise ValueError("Months must be positive.")
            expiry_date = joining_date + relativedelta(months=no_months)
        except Exception as e:
            return Response(
                {"message": "Invalid months value.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        TblSession.objects.filter(user_id=user_id).update(
            is_active=False, deleted_at=timezone.now()
        )

        key = uuid.uuid4()

        session = TblSession.objects.create(
            user=user,
            key=key,
            joining_date=joining_date,
            expiry_date=expiry_date,
            is_active=is_active,
        )

        serializer = TblSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SessionKeyRegenerateView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def put(self, request, user_id):

        try:
            session = TblSession.objects.filter(
                user=user_id, deleted_at__isnull=True
            ).latest("id")
        except TblSession.DoesNotExist:
            return Response(
                {"message": "Active session for this user does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        session.key = uuid.uuid4()
        session.save()

        serializer = TblSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SessionStatusUpdateView(APIView):

    permission_classes = [IsAuthenticated, IsSessionActive]

    def put(self, request, user_id):
        session = (
            TblSession.objects.filter(user=user_id, deleted_at__isnull=True)
            .order_by("-id")
            .first()
        )

        if not session:
            return Response(
                {"detail": "No active session found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        is_active = request.data.get("is_active")
        if not isinstance(is_active, bool):
            return Response(
                {"detail": "'is_active' must be a boolean (true or false)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.is_active = is_active
        session.save()

        return Response(
            {"detail": f"Session marked as {'active' if is_active else 'inactive'}."},
            status=status.HTTP_200_OK,
        )


class RenewSessionView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def put(self, request, user_id):
        joining_date_str = request.data.get("joining_date")
        no_months = request.data.get("months")
        is_active = request.data.get("is_active", True)

        if not joining_date_str or no_months is None:
            return Response(
                {"message": "joining_date and months are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = TblUser.objects.get(
                id=user_id, is_active=True, deleted_at__isnull=True
            )
        except TblUser.DoesNotExist:
            return Response(
                {"message": f"User with ID {user_id} does not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            joining_date = datetime.strptime(joining_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"message": "Invalid joining_date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            no_months = int(no_months)
            if no_months <= 0:
                raise ValueError("Months must be a positive number.")
        except Exception as e:
            return Response(
                {"message": "Invalid months value.", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        today = timezone.now().date()

        try:
            session = TblSession.objects.filter(
                user=user,
                is_active=True,
                deleted_at__isnull=True,
            ).latest("expiry_date")
        except TblSession.DoesNotExist:
            session = None

        if session and session.expiry_date >= today:

            session.expiry_date += relativedelta(months=no_months)
            session.is_active = is_active
            session.save()
            message = f"Session expiry extended by {no_months} month(s)."
        else:

            TblSession.objects.filter(user=user).update(
                is_active=False, deleted_at=timezone.now()
            )

            key = uuid.uuid4()
            expiry_date = joining_date + relativedelta(months=no_months)

            session = TblSession.objects.create(
                user=user,
                key=key,
                joining_date=joining_date,
                expiry_date=expiry_date,
                is_active=is_active,
            )

            message = f"New session created for {no_months} month(s)."

        serializer = TblSessionSerializer(session)
        return Response(
            {
                "status": "success",
                "message": message,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
