from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Max
from rest_framework.permissions import AllowAny
from loan.models.LoanAccount import LoanAccount
from ..serializers.loan_account_serializer import LoanAccountSerializer
from users.permissions.is_user_session_key_valid import SessionKeyAuthentication
from users.utils.session_key_log_utils import log_session_key_usage
from users.utils.pagination import CustomPagination

from constants import (
    LOAN_ACCOUNT_EXISTS_CHECK,
    CUSTOMER_LOGIN_SEARCH,
    LOAN_ACCOUNT_FLEXIBLE_SEARCH,
    RECENT_LOAN_PAYMENT_DETAIL,
)
from django.utils.timezone import now


class CustomerLoginSearch(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = CUSTOMER_LOGIN_SEARCH

        mobile_number = request.query_params.get("mobileNumber")
        loan_id = request.query_params.get("loanId")
        loan_account = request.query_params.get("loanAccount")

        query = Q()
        if mobile_number:
            query |= Q(primary_mobile_number=mobile_number)
        if loan_id:
            query |= Q(loan_id=loan_id)
        if loan_account:
            query |= Q(loan_account=loan_account)

        if not query:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "detail": "At least one query parameter (mobileNumber, loanId, or loanAccount) must be provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        filtered_accounts = LoanAccount.objects.filter(query, mis_date=latest_date)
        if not filtered_accounts.exists():
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"detail": "No records found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        results = [
            {"primary_mobile_number": acc.primary_mobile_number, "loan_id": acc.loan_id}
            for acc in filtered_accounts
        ]

        log_session_key_usage(request, endpoint_name, status="success")
        return Response(
            {
                "count": len(results),
                "created_date": str(latest_date),
                "results": results,
            },
            status=status.HTTP_200_OK,
        )


class LoanAccountFlexibleSearch(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = LOAN_ACCOUNT_FLEXIBLE_SEARCH

        mobile_number = request.query_params.get("mobileNumber")
        aadhar_number = request.query_params.get("aadharNumber")
        pan = request.query_params.get("panNumber")
        loan_account = request.query_params.get("loanAccount")
        loan_id = request.query_params.get("loanId")

        query = Q()
        if mobile_number:
            query |= Q(primary_mobile_number=mobile_number)
        if aadhar_number:
            query |= Q(aadhar_no=aadhar_number)
        if pan:
            query |= Q(pan=pan)
        if loan_account:
            query |= Q(loan_account=loan_account)
        if loan_id:
            query |= Q(loan_id=loan_id)

        if not query:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"detail": "At least one query parameter must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        accounts = LoanAccount.objects.filter(query, mis_date=latest_date)
        if not accounts.exists():
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"detail": "No records found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LoanAccountSerializer(accounts, many=True)
        log_session_key_usage(request, endpoint_name, status="success")

        return Response(
            {
                "count": accounts.count(),
                "mis_date": str(latest_date),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class RecentLoanPaymentDetailView(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = RECENT_LOAN_PAYMENT_DETAIL

        loan_account = request.query_params.get("loanAccount")
        loan_id = request.query_params.get("loanId")

        if not loan_account and not loan_id:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"detail": "Please provide either 'loanAccount' or 'loanId'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        query = Q()
        if loan_account:
            query |= Q(loan_account=loan_account)
        if loan_id:
            query |= Q(loan_id=loan_id)

        today = now().date()
        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        latest_account = (
            LoanAccount.objects.filter(query, mis_date=latest_date)
            .order_by("-mis_date")
            .first()
        )

        if not latest_account:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"detail": "No recent record found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = LoanAccountSerializer(latest_account)

        log_session_key_usage(request, endpoint_name, status="success")
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoanAccountExistsCheck(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def post(self, request):
        endpoint_name = LOAN_ACCOUNT_EXISTS_CHECK

        loan_account = request.data.get("loanAccount")
        loan_id = request.data.get("loanId")
        mobile_number = request.data.get("mobileNumber")

        if not loan_account and not loan_id and not mobile_number:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "error": "At least one of 'loanAccount', 'loanId', or 'mobileNumber' must be provided."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        query = Q()
        if loan_account:
            query |= Q(loan_account=loan_account)
        if loan_id:
            query |= Q(loan_id=loan_id)
        if mobile_number:
            query |= Q(primary_mobile_number=mobile_number)

        today = now().date()
        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        exists = LoanAccount.objects.filter(query, mis_date=latest_date).exists()

        log_session_key_usage(request, endpoint_name, status="success")

        return Response({"status": exists}, status=status.HTTP_200_OK)
