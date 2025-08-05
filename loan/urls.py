from django.urls import path
from loan.views.loan_view import (
    CustomerLoginSearch,
    LoanAccountExistsCheck,
    LoanAccountFlexibleSearch,
    RecentLoanPaymentDetailView,
)
from loan.views.customer_view import (
    AllCustomersView,
    CustomerAddressSearchView,
    CustomerCountView,
    CustomerFlexibleSearchView,
)

urlpatterns = [
    path(
        "customer_login/",
        CustomerLoginSearch.as_view(),
        name="customer-login-search",
    ),
    path(
        "loan-account/",
        LoanAccountFlexibleSearch.as_view(),
        name="loan-account-flexible-search",
    ),
    path(
        "check-loan-account/",
        LoanAccountExistsCheck.as_view(),
        name="check-loan-account",
    ),
    path(
        "recent-loan-payment/",
        RecentLoanPaymentDetailView.as_view(),
        name="recent-loan-payment-detail",
    ),
    path("customers/get-all/", AllCustomersView.as_view(), name="all-customers"),
    path("customers/count/", CustomerCountView.as_view(), name="customer-count"),
    path(
        "customers/search/",
        CustomerFlexibleSearchView.as_view(),
        name="customer-search",
    ),
    path(
        "customers/getBy-account-number/",
        LoanAccountFlexibleSearch.as_view(),
        name="loan-account-flexible-search",
    ),
    path(
        "customers/search-by-address/",
        CustomerAddressSearchView.as_view(),
        name="customer-search-by-address",
    ),
]
