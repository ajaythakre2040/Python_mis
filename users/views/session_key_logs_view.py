from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from users.models import SessionKeyUsageLog
from users.permissions.session_active import IsSessionActive
from users.serializers import SessionKeyUsageLogSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.dateparse import parse_date
from datetime import datetime, time
from users.utils.pagination import CustomPagination
from collections import OrderedDict


class SessionKeyUsageSummaryView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request, user_id=None):
        logs = SessionKeyUsageLog.objects.all()

        if user_id is not None:
            logs = logs.filter(user_id=user_id)
            if not logs.exists():
                return Response(
                    {"message": "No logs found for the specified user."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        summary = (
            logs.values("user_id", "endpoint")
            .annotate(
                total_uses=Count("id"),
                success_count=Count("id", filter=Q(status="success")),
                failed_count=Count("id", filter=Q(status="failed")),
            )
            .order_by("user_id", "endpoint")
        )

        return Response(
            {
                "message": "Session key usage summary retrieved successfully.",
                "data": summary,
            },
            status=status.HTTP_200_OK,
        )


class SessionLogkeyFilterView(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):
        params = request.query_params

        user_id = params.get("user_id")
        endpoint = params.get("endpoint")
        from_date_str = params.get("from_date")
        to_date_str = params.get("to_date")

        logs = SessionKeyUsageLog.objects.select_related("user").all()

        if user_id:
            logs = logs.filter(user_id=user_id)

        if endpoint:
            logs = logs.filter(endpoint=endpoint)

        if from_date_str and to_date_str:
            from_date = parse_date(from_date_str)
            to_date = parse_date(to_date_str)

            if not from_date or not to_date:
                return Response(
                    {"detail": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            start_datetime = datetime.combine(from_date, time.min)
            end_datetime = datetime.combine(to_date, time.max)

            logs = logs.filter(used_at__range=(start_datetime, end_datetime))

        elif from_date_str or to_date_str:
            return Response(
                {"detail": "Both from_date and to_date must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not logs.exists():
            return Response(
                {"message": "No logs found."}, status=status.HTTP_404_NOT_FOUND
            )

        stats = logs.aggregate(
            total=Count("id"),
            total_success=Count("id", filter=Q(status="success")),
            total_failed=Count("id", filter=Q(status="failed")),
        )

        paginator = CustomPagination()
        paginated_logs = paginator.paginate_queryset(logs, request)
        serializer = SessionKeyUsageLogSerializer(paginated_logs, many=True)

        extra_fields = OrderedDict(
            [
                ("message", "Logs retrieved successfully."),
                (
                    "filters_used",
                    {
                        "user_id": user_id,
                        "endpoint": endpoint,
                        "from_date": from_date_str,
                        "to_date": to_date_str,
                    },
                ),
                ("stats", stats),
            ]
        )

        return paginator.get_custom_paginated_response(serializer.data, extra_fields)


class EndpointsList(APIView):
    permission_classes = [IsAuthenticated, IsSessionActive]

    def get(self, request):

        endpoints = SessionKeyUsageLog.objects.values_list(
            "endpoint", flat=True
        ).distinct()

        return Response(
            {
                "status": "success",
                "count": endpoints.count(),
                "endpoints": list(endpoints),
            },
            status=status.HTTP_200_OK,
        )
