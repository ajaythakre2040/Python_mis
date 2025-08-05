from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from users.models import TblUser, TblSession
from users.serializers.userSerializer import (
    TblUserSerializer,
    TblUserWithSessionsSerializer,
)
from users.permissions.session_active import IsSessionActive
from django.db.models import Q
from users.utils.pagination import CustomPagination


class UsersListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):
        users = TblUser.objects.filter(is_active=True, deleted_at__isnull=True)

        if not users.exists():
            return Response(
                {
                    "status": "error",
                    "message": "No active users found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = TblUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TblUserSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "message": "User created successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "status": "error",
                "message": "User creation failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get_object(self, pk):
        try:
            return TblUser.objects.get(pk=pk, is_active=True, deleted_at__isnull=True)
        except TblUser.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(
                {
                    "status": "error",
                    "message": f"User with ID {pk} not found or inactive.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        expired_sessions = TblSession.objects.filter(
            user=user,
            expiry_date__lt=date.today(),
            deleted_at__isnull=True,
        )

        expired_sessions_count = expired_sessions.update(is_active=False)

        if expired_sessions_count > 0:
            session_status_message = (
                f"expired session(s) were deactivated for this user."
            )
        else:
            session_status_message = "No expired sessions found for this user."

        serializer = TblUserWithSessionsSerializer(user)

        return Response(
            {
                "status": "success",
                "message": session_status_message,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(
                {
                    "status": "error",
                    "message": f"User with ID {pk} not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TblUserSerializer(
            user, data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "User updated successfully.",
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {
                "status": "error",
                "message": "User update failed.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        user = self.get_object(pk)
        if not user:
            return Response(
                {
                    "status": "error",
                    "message": f"User with ID {pk} not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()
        return Response(
            {
                "status": "success",
                "message": "User deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )


class UsersCountView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):

        total_users = TblUser.objects.filter(
            is_active=True, deleted_at__isnull=True
        ).count()

        total_users_sessions = TblSession.objects.filter(
            deleted_at__isnull=True
        ).count()

        active_session_users = (
            TblSession.objects.filter(is_active=True, deleted_at__isnull=True)
            .distinct()
            .count()
        )
        user_session_not_create = total_users - total_users_sessions

        inactive_session_users = total_users_sessions - active_session_users

        return Response(
            {
                "status": "success",
                "total_users": total_users,
                "total_users_session": total_users_sessions,
                "user_session_not_create": user_session_not_create,
                "active_session_users": active_session_users,
                "inactive_session_users": inactive_session_users,
            },
            status=status.HTTP_200_OK,
        )


class UsersSearchAPIView(APIView):

    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):
        query = request.GET.get("query", "").strip()

        if not query:
            return Response(
                {
                    "status": "error",
                    "message": "Missing required query parameter 'query'.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        users = TblUser.objects.filter(is_active=True, deleted_at__isnull=True)

        users = users.filter(
            Q(fullname__icontains=query)
            | Q(mobileno__icontains=query)
            | Q(email__icontains=query)
            | Q(address__icontains=query)
            | Q(gstno__icontains=query)
        )

        if not users.exists():
            return Response(
                {
                    "status": "error",
                    "message": "No users found matching the search criteria.",
                    "count": 0,
                    "results": [],
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(users, request)
        serializer = TblUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializer.data)


class UsersNameList(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):
        users = TblUser.objects.filter(is_active=True, deleted_at__isnull=True)
        serializer = TblUserSerializer(users, many=True)
        return Response(
            {
                "status": "success",
                "count": users.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
