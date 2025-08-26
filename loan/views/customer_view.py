import re
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
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from constants import (
    ALL_CUSTOMERS_LIST,
    CUSTOMER_TOTAL_COUNT,
    CUSTOMER_FLEXIBLE_SEARCH,
    CUSTOMER_SEARCH_BY_ADDRESS,
)
from rapidfuzz import fuzz

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


# 18-8-25
# class CustomerAddressSearchView(APIView):
#     authentication_classes = [SessionKeyAuthentication]

#     def get(self, request):
#         endpoint_name = CUSTOMER_SEARCH_BY_ADDRESS
#         address = request.GET.get("address", "").strip()
#         zipcode = request.GET.get("zipcode", "").strip()

#         if not address or not zipcode:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Address and Zipcode are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not re.fullmatch(r"\d{6}", zipcode):
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Zipcode must be a valid 6-digit number.",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         clean_address = re.sub(r"[^\w\s]", " ", address)
#         clean_address = re.sub(r"\s+", " ", clean_address)
#         keywords = [word.lower() for word in clean_address.split() if word]

#         if not keywords:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Invalid address format.", "data": []},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         total_keywords = len(keywords)

#         def fetch_records(cursor, query, params):
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             return [dict(zip(columns, row)) for row in cursor.fetchall()]

#         def compute_exact_match_score(address_text, keywords):

#             address_words = address_text.lower().split()
#             return sum(1 for kw in keywords if kw in address_words)

#         def compute_fuzzy_match_score(address_text, keywords):

#             address_words = address_text.lower().split()
#             total_score = 0.0
#             for kw in keywords:
#                 scores = [fuzz.ratio(kw, w) for w in address_words]
#                 max_score = max(scores) if scores else 0
#                 if max_score >= 80:
#                     total_score += max_score / 100
#             return total_score

#         try:
#             results = []
#             with connections["readonly"].cursor() as cursor:
#                 queries = [
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             customer_name,
#                             customer_address,
#                             zipcode,
#                             mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'customer' AS ctype
#                         FROM dedup_api_1
#                         WHERE zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             coapplicant_customer_name AS customer_name,
#                             coapplicant_full_address AS customer_address,
#                             coapplicant_zipcode AS zipcode,
#                             coapplicant_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'coapplicant' AS ctype
#                         FROM dedup_api_1
#                         WHERE coapplicant_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             guarantor_customer_name AS customer_name,
#                             guarantor_full_address AS customer_address,
#                             guarantor_zipcode AS zipcode,
#                             guarantor_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'guarantor' AS ctype
#                         FROM dedup_api_1
#                         WHERE guarantor_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                 ]

#                 for query, params in queries:
#                     fetched = fetch_records(cursor, query, params)
#                     results.extend(fetched)

#             for record in results:
#                 addr = record.get("customer_address") or ""
#                 record["exact_match_score"] = compute_exact_match_score(addr, keywords)
#                 record["fuzzy_match_score"] = compute_fuzzy_match_score(addr, keywords)

#             exact_matches = [r for r in results if r["exact_match_score"] > 0]
#             for r in exact_matches:
#                 r["match_score"] = r["exact_match_score"]
#                 r["match_type"] = "exact"
#                 r["match_percentage"] = round(
#                     (r["exact_match_score"] / total_keywords) * 100, 2
#                 )

#             exact_matches.sort(key=lambda r: (-r["match_score"], r["loan_id"]))

#             if len(exact_matches) < 15:
#                 exact_loan_ids = {r["loan_id"] for r in exact_matches}
#                 fuzzy_candidates = [
#                     r
#                     for r in results
#                     if r["fuzzy_match_score"] > 0 and r["loan_id"] not in exact_loan_ids
#                 ]
#                 for r in fuzzy_candidates:
#                     r["match_score"] = r["fuzzy_match_score"]
#                     r["match_type"] = "fuzzy"
#                     r["match_percentage"] = round(
#                         (r["fuzzy_match_score"] / total_keywords) * 100, 2
#                     )

#                 fuzzy_candidates.sort(key=lambda r: (-r["match_score"], r["loan_id"]))
#                 fuzzy_matches = fuzzy_candidates[: (15 - len(exact_matches))]
#             else:
#                 fuzzy_matches = []

#             final_results = exact_matches + fuzzy_matches
#             final_results = final_results[:15]

#             log_session_key_usage(request, endpoint_name, status="success")

#             if not final_results:
#                 return Response(
#                     {
#                         "success": True,
#                         "status_code": 200,
#                         "message": "No matching records found.",
#                         "data": [],
#                     },
#                     status=status.HTTP_200_OK,
#                 )

#             return Response(
#                 {
#                     "success": True,
#                     "status_code": 200,
#                     "message": f"{len(final_results)} best-matching record(s) found.",
#                     "data": final_results,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "status_code": 500,
#                     "message": "An error occurred while accessing the database.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )

# 19-8-25
# class CustomerAddressSearchView(APIView):
#     authentication_classes = [SessionKeyAuthentication]

#     def get(self, request):
#         endpoint_name = CUSTOMER_SEARCH_BY_ADDRESS
#         address = request.GET.get("address", "").strip()
#         zipcode = request.GET.get("zipcode", "").strip()

#         if not address or not zipcode:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Address and Zipcode are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not re.fullmatch(r"\d{6}", zipcode):
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Zipcode must be a valid 6-digit number.",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         clean_address = re.sub(r"[^\w\s]", " ", address)
#         clean_address = re.sub(r"\s+", " ", clean_address)
#         keywords = [word.lower() for word in clean_address.split() if word]

#         if not keywords:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Invalid address format.", "data": []},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         total_keywords = len(keywords)

#         def fetch_records(cursor, query, params):
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             return [dict(zip(columns, row)) for row in cursor.fetchall()]

#         def compute_exact_match_score(address_text, keywords):

#             address_words = address_text.lower().split()
#             return sum(1 for kw in keywords if kw in address_words)

#         # def compute_fuzzy_match_score(address_text, keywords):

#         #     address_words = address_text.lower().split()
#         #     total_score = 0.0
#         #     for kw in keywords:
#         #         scores = [fuzz.ratio(kw, w) for w in address_words]
#         #         max_score = max(scores) if scores else 0
#         #         if max_score >= 80:
#         #             total_score += max_score / 100
#         #     return total_score
#         def compute_fuzzy_match_score(address_text, keywords):
#             address_text_lower = address_text.lower()
#             total_score = 0.0
#             for kw in keywords:

#                 full_score = fuzz.partial_ratio(kw, address_text_lower)
#                 word_scores = [fuzz.ratio(kw, w) for w in address_text_lower.split()]
#                 max_word_score = max(word_scores) if word_scores else 0


#                 max_score = max(full_score, max_word_score)
#                 if max_score >= 80:
#                     total_score += max_score / 100

#             return total_score

#         try:
#             results = []
#             with connections["readonly"].cursor() as cursor:
#                 queries = [
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             customer_name,
#                             customer_address,
#                             zipcode,
#                             mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'customer' AS ctype
#                         FROM dedup_api_1
#                         WHERE zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             coapplicant_customer_name AS customer_name,
#                             coapplicant_full_address AS customer_address,
#                             coapplicant_zipcode AS zipcode,
#                             coapplicant_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'coapplicant' AS ctype
#                         FROM dedup_api_1
#                         WHERE coapplicant_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             guarantor_customer_name AS customer_name,
#                             guarantor_full_address AS customer_address,
#                             guarantor_zipcode AS zipcode,
#                             guarantor_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'guarantor' AS ctype
#                         FROM dedup_api_1
#                         WHERE guarantor_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                 ]

#                 for query, params in queries:
#                     fetched = fetch_records(cursor, query, params)
#                     results.extend(fetched)

#             for record in results:
#                 addr = record.get("customer_address") or ""
#                 record["exact_match_score"] = compute_exact_match_score(addr, keywords)
#                 record["fuzzy_match_score"] = compute_fuzzy_match_score(addr, keywords)

#             exact_matches = [r for r in results if r["exact_match_score"] > 0]
#             for r in exact_matches:
#                 r["match_score"] = r["exact_match_score"]
#                 r["match_type"] = "exact"
#                 r["match_percentage"] = round(
#                     (r["exact_match_score"] / total_keywords) * 100, 2
#                 )

#             exact_matches.sort(key=lambda r: (-r["match_score"], r["loan_id"]))

#             if len(exact_matches) < 15:
#                 exact_loan_ids = {r["loan_id"] for r in exact_matches}
#                 fuzzy_candidates = [
#                     r
#                     for r in results
#                     if r["fuzzy_match_score"] > 0 and r["loan_id"] not in exact_loan_ids
#                 ]
#                 for r in fuzzy_candidates:
#                     r["match_score"] = r["fuzzy_match_score"]
#                     r["match_type"] = "fuzzy"
#                     r["match_percentage"] = round(
#                         (r["fuzzy_match_score"] / total_keywords) * 100, 2
#                     )

#                 fuzzy_candidates.sort(key=lambda r: (-r["match_score"], r["loan_id"]))
#                 fuzzy_matches = fuzzy_candidates[: (15 - len(exact_matches))]
#             else:
#                 fuzzy_matches = []

#             final_results = exact_matches + fuzzy_matches
#             final_results = final_results[:15]

#             log_session_key_usage(request, endpoint_name, status="success")

#             if not final_results:
#                 return Response(
#                     {
#                         "success": True,
#                         "status_code": 200,
#                         "message": "No matching records found.",
#                         "data": [],
#                     },
#                     status=status.HTTP_200_OK,
#                 )

#             return Response(
#                 {
#                     "success": True,
#                     "status_code": 200,
#                     "message": f"{len(final_results)} best-matching record(s) found.",
#                     "data": final_results,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "status_code": 500,
#                     "message": "An error occurred while accessing the database.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )


COMMON_SUFFIXES = [
    "nagar",
    "vihar",
    "colony",
    "basti",
    "road",
    "marg",
    "puram",
    "gaon",
    "pura",
    "bagh",
    "town",
    "old",
    "new",
    "area",
    "urban",
    "mohalla",
    "vastu",
    "surji",
    "pet",
    "taluka",
    "city",
    "chowk",
    "chok",
    "galli",
    "peth",
    "wadi",
    "tanda",
    "bazar",
    "vasti",
    "gate",
    "local",
    "para",
    "pada",
    "wada",
]


def smart_split_keywords(address):
    address = address.lower()
    clean_address = re.sub(r"[^\w\s]", " ", address)
    clean_address = re.sub(r"\s+", " ", clean_address).strip()
    words = clean_address.split()
    result = []

    for word in words:
        matched = False
        for suffix in COMMON_SUFFIXES:
            if word.endswith(suffix) and word != suffix:
                prefix = word[: -len(suffix)]
                if prefix:
                    result.append(prefix)
                    result.append(suffix)
                    matched = True
                    break
        if not matched:
            result.append(word)

    return list(set(result))


class CustomerAddressSearchView(APIView):
    authentication_classes = [SessionKeyAuthentication]

    def get(self, request):
        endpoint_name = CUSTOMER_SEARCH_BY_ADDRESS
        address = request.GET.get("address", "").strip()
        zipcode = request.GET.get("zipcode", "").strip()

        if not address or not zipcode:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"success": False, "message": "Address and Zipcode are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not re.fullmatch(r"\d{6}", zipcode):
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "success": False,
                    "message": "Zipcode must be a valid 6-digit number.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        keywords = smart_split_keywords(address)

        if not keywords:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {"success": False, "message": "Invalid address format.", "data": []},
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_keywords = len(keywords)

        def fetch_records(cursor, query, params):
            cursor.execute(query, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

        def compute_exact_match_score(address_text, keywords):
            address_words = smart_split_keywords(address_text)
            return sum(1 for kw in keywords if kw in address_words)

        def compute_fuzzy_match_score(address_text, keywords):
            address_words = smart_split_keywords(address_text)
            total_score = 0.0
            for kw in keywords:
                scores = [fuzz.ratio(kw, word) for word in address_words]
                max_score = max(scores) if scores else 0
                if max_score >= 80:
                    total_score += max_score / 100
            return round(total_score, 2)

        try:
            results = []
            with connections["readonly"].cursor() as cursor:
                queries = [
                    (
                        """
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
                        WHERE zipcode = %s
                        """,
                        [zipcode],
                    ),
                    (
                        """
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
                        WHERE coapplicant_zipcode = %s
                        """,
                        [zipcode],
                    ),
                    (
                        """
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
                        WHERE guarantor_zipcode = %s
                        """,
                        [zipcode],
                    ),
                ]

                for query, params in queries:
                    fetched = fetch_records(cursor, query, params)
                    results.extend(fetched)

            for record in results:
                addr = record.get("customer_address") or ""
                record["exact_match_score"] = compute_exact_match_score(addr, keywords)
                record["fuzzy_match_score"] = compute_fuzzy_match_score(addr, keywords)

            exact_matches = [r for r in results if r["exact_match_score"] > 0]
            for r in exact_matches:
                r["match_score"] = r["exact_match_score"]
                r["match_type"] = "exact"
                r["match_percentage"] = round(
                    (r["exact_match_score"] / total_keywords) * 100, 2
                )

            exact_matches.sort(key=lambda r: (-r["match_score"], r["loan_id"]))

            if len(exact_matches) < 15:
                exact_loan_ids = {r["loan_id"] for r in exact_matches}
                fuzzy_candidates = [
                    r
                    for r in results
                    if r["fuzzy_match_score"] > 0 and r["loan_id"] not in exact_loan_ids
                ]
                for r in fuzzy_candidates:
                    r["match_score"] = r["fuzzy_match_score"]
                    r["match_type"] = "fuzzy"
                    r["match_percentage"] = round(
                        (r["fuzzy_match_score"] / total_keywords) * 100, 2
                    )

                fuzzy_candidates.sort(key=lambda r: (-r["match_score"], r["loan_id"]))
                fuzzy_matches = fuzzy_candidates[: (15 - len(exact_matches))]
            else:
                fuzzy_matches = []

            final_results = exact_matches + fuzzy_matches
            final_results = final_results[:15]
            for record in final_results:
                record.pop("exact_match_score", None)
                record.pop("fuzzy_match_score", None)
                record.pop("match_score", None)
                record.pop("match_type", None)
            log_session_key_usage(request, endpoint_name, status="success")

            if not final_results:
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
                    "message": f"{len(final_results)} best-matching record(s) found.",
                    "data": final_results,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            log_session_key_usage(request, endpoint_name, status="failed")
            return Response(
                {
                    "success": False,
                    "status_code": 500,
                    "message": "An error occurred while accessing the database.",
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# # 17-8-25
# class CustomerAddressSearchView(APIView):
#     authentication_classes = [SessionKeyAuthentication]

#     def get(self, request):
#         endpoint_name = CUSTOMER_SEARCH_BY_ADDRESS
#         address = request.GET.get("address", "").strip()
#         zipcode = request.GET.get("zipcode", "").strip()

#         if not address or not zipcode:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Address and Zipcode are required."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if not re.fullmatch(r"\d{6}", zipcode):
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "message": "Zipcode must be a valid 6-digit number.",
#                 },
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         clean_address = re.sub(r"[^\w\s]", " ", address)
#         clean_address = re.sub(r"\s+", " ", clean_address)
#         keywords = [word.lower() for word in clean_address.split() if word]

#         if not keywords:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {"success": False, "message": "Invalid address format.", "data": []},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         total_keywords = len(keywords)

#         def fetch_records(cursor, query, params):
#             cursor.execute(query, params)
#             columns = [col[0] for col in cursor.description]
#             return [dict(zip(columns, row)) for row in cursor.fetchall()]

#         def compute_fuzzy_match_score(address_text, keywords):

#             address_lower = address_text.lower()
#             return sum(
#                 1 for kw in keywords if fuzz.partial_ratio(kw, address_lower) >= 80
#             )

#         try:
#             results = []
#             with connections["readonly"].cursor() as cursor:
#                 queries = [
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             customer_name,
#                             customer_address,
#                             zipcode,
#                             mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'customer' AS ctype
#                         FROM dedup_api_1
#                         WHERE zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             coapplicant_customer_name AS customer_name,
#                             coapplicant_full_address AS customer_address,
#                             coapplicant_zipcode AS zipcode,
#                             coapplicant_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'coapplicant' AS ctype
#                         FROM dedup_api_1
#                         WHERE coapplicant_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                     (
#                         """
#                         SELECT
#                             loan_account,
#                             loan_id,
#                             guarantor_customer_name AS customer_name,
#                             guarantor_full_address AS customer_address,
#                             guarantor_zipcode AS zipcode,
#                             guarantor_mobile_no AS mobile_no,
#                             scheme_name,
#                             branch_name,
#                             disbursal_date,
#                             total_outstanding,
#                             total_overdue,
#                             repo_flag,
#                             loan_status,
#                             'guarantor' AS ctype
#                         FROM dedup_api_1
#                         WHERE guarantor_zipcode = %s
#                         """,
#                         [zipcode],
#                     ),
#                 ]
#                 for query, params in queries:
#                     fetched = fetch_records(cursor, query, params)
#                     results.extend(fetched)

#             for record in results:
#                 addr = record.get("customer_address") or ""
#                 record["match_score"] = compute_fuzzy_match_score(addr, keywords)
#                 record["match_percentage"] = round(
#                     (record["match_score"] / total_keywords) * 100, 2
#                 )

#             results = [r for r in results if r["match_score"] > 0]

#             results.sort(key=lambda r: (-r["match_score"], r["loan_id"]))

#             results = results[:15]

#             log_session_key_usage(request, endpoint_name, status="success")

#             if not results:
#                 return Response(
#                     {
#                         "success": True,
#                         "status_code": 200,
#                         "message": "No matching records found.",
#                         "data": [],
#                     },
#                     status=status.HTTP_200_OK,
#                 )

#             return Response(
#                 {
#                     "success": True,
#                     "status_code": 200,
#                     "message": f"{len(results)} best-matching record(s) found.",
#                     "data": results,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except Exception as e:
#             log_session_key_usage(request, endpoint_name, status="failed")
#             return Response(
#                 {
#                     "success": False,
#                     "status_code": 500,
#                     "message": "An error occurred while accessing the database.",
#                     "error": str(e),
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
