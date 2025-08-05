from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Max
from rest_framework.permissions import AllowAny
from loan.models import LoanAccount, DedupApi
from users.utils.pagination import CustomPagination
from ..serializers.loan_account_serializer import LoanAccountSerializer
from users.permissions.is_user_session_key_valid import SessionKeyAuthentication
from users.utils.session_key_log_utils import log_session_key_usage
from django.utils.timezone import now

from constants import (
    ALL_CUSTOMERS_LIST,
    CUSTOMER_TOTAL_COUNT,
    CUSTOMER_FLEXIBLE_SEARCH,
    CUSTOMER_SEARCH_BY_ADDRESS,
)

from django.db import connections



class AllCustomersView(GenericAPIView):
    authentication_classes = [SessionKeyAuthentication]
    serializer_class = LoanAccountSerializer
    pagination_class = CustomPagination

    def get(self, request):
        endpoint_name = ALL_CUSTOMERS_LIST
        today = now().date()
        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        queryset = LoanAccount.objects.filter(mis_date=latest_date)
        if not queryset.exists():
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"status": "error", "message": "No customers found for today."},
                status=status.HTTP_404_NOT_FOUND,
            )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        log_session_key_usage(request, endpoint_name, status="success")
        return self.get_paginated_response(serializer.data)


class CustomerCountView(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = CUSTOMER_TOTAL_COUNT
        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        total_count = LoanAccount.objects.filter(mis_date=latest_date).count()
        log_session_key_usage(request, endpoint_name, status="success")
        return Response({"total_customers": total_count}, status=status.HTTP_200_OK)


class CustomerFlexibleSearchView(GenericAPIView):
    authentication_classes = [SessionKeyAuthentication]
    serializer_class = LoanAccountSerializer
    pagination_class = CustomPagination

    def get(self, request):
        endpoint_name = CUSTOMER_FLEXIBLE_SEARCH
        search_value = request.query_params.get("query")
        if not search_value:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "status": "error",
                    "message": "Missing required query parameter: 'query'.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        query = (
            Q(customer_name__icontains=search_value)
            | Q(primary_mobile_number__icontains=search_value)
            | Q(loan_id__icontains=search_value)
            | Q(loan_account__icontains=search_value)
            | Q(pan__icontains=search_value)
            | Q(aadhar_no__icontains=search_value)
        )
        latest_date = LoanAccount.objects.aggregate(latest_date=Max("mis_date"))[
            "latest_date"
        ]
        queryset = LoanAccount.objects.filter(query, mis_date=latest_date)
        if not queryset.exists():
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"status": "error", "message": "No matching customers found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        log_session_key_usage(request, endpoint_name, status="success")
        return self.get_paginated_response(serializer.data)


class CustomerAddressSearchView(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = CUSTOMER_SEARCH_BY_ADDRESS
        address = request.GET.get("address", "").strip()
        zipcode = request.GET.get("zipcode", "").strip()

        if not address or not zipcode:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "success": False,
                    "message": "Address and Zipcode are required.",
                    "data": [],
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        keywords = [word for word in address.split() if word]

        if not keywords:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"success": False, "message": "Invalid address format.", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        def build_conditions(field_name):
            return " AND ".join([f"{field_name} ILIKE %s" for _ in keywords])

        def fetch_records(cursor, query, params):
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        try:
            results = []
            with connections["readonly"].cursor() as cursor:

                customer_query = f"""
                    SELECT 
                        loan_account,
                        loan_id,
                        customer_name,
                        customer_address,
                        zipcode,
                        mobile_no,
                        scheme_name,
                        branch_name,
                        disbursal_date,
                        total_outstanding,
                        total_overdue,
                        repo_flag,
                        loan_status,
                        'customer' AS ctype
                    FROM dedup_api_1
                    WHERE zipcode = %s AND {build_conditions("customer_address")}
                    LIMIT 5;
                """
                customer_params = [zipcode] + [f"%{kw}%" for kw in keywords]
                results.extend(fetch_records(cursor, customer_query, customer_params))

                coapplicant_query = f"""
                    SELECT 
                        loan_account,
                        loan_id,
                        coapplicant_customer_name AS customer_name,
                        coapplicant_full_address AS customer_address,
                        coapplicant_zipcode AS zipcode,
                        coapplicant_mobile_no AS mobile_no,
                        scheme_name,
                        branch_name,
                        disbursal_date,
                        total_outstanding,
                        total_overdue,
                        repo_flag,
                        loan_status,
                        'coapplicant' AS ctype
                    FROM dedup_api_1
                    WHERE coapplicant_zipcode = %s AND {build_conditions("coapplicant_full_address")}
                    LIMIT 5;
                """
                coapplicant_params = [zipcode] + [f"%{kw}%" for kw in keywords]
                results.extend(
                    fetch_records(cursor, coapplicant_query, coapplicant_params)
                )

                guarantor_query = f"""
                    SELECT 
                        loan_account,
                        loan_id,
                        guarantor_customer_name AS customer_name,
                        guarantor_full_address AS customer_address,
                        guarantor_zipcode AS zipcode,
                        guarantor_mobile_no AS mobile_no,
                        scheme_name,
                        branch_name,
                        disbursal_date,
                        total_outstanding,
                        total_overdue,
                        repo_flag,
                        loan_status,
                        'guarantor' AS ctype
                    FROM dedup_api_1
                    WHERE guarantor_zipcode = %s AND {build_conditions("guarantor_full_address")}
                    LIMIT 5;
                """
                guarantor_params = [zipcode] + [f"%{kw}%" for kw in keywords]
                results.extend(fetch_records(cursor, guarantor_query, guarantor_params))

            log_session_key_usage(request, endpoint_name, status="success")
            if not results:
                return Response(
                    {
                        "success": True,
                        "status_code": 200,
                        "message": "No matching records found.",
                        "data": [],
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {
                    "success": True,
                    "status_code": 200,
                    "message": f"{len(results[:15])} record(s) found.",
                    "data": results[:15],
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "success": False,
                    "message": "An error occurred while accessing the database.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
