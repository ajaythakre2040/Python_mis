from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views.auth_views import (
    RegisterUserView,
    LoginUserView,
    LogoutUserView,
    ResetPasswordView,
)


from users.views.user_view import (
    UsersCountView,
    UsersListCreateAPIView,
    UserDetailAPIView,
    UsersNameList,
    UsersSearchAPIView,
)
from users.views.user_session_view import (
    UserSessionCreateView,
    SessionKeyRegenerateView,
    SessionStatusUpdateView,
    RenewSessionView,
)

from users.views.session_key_logs_view import (
    EndpointsList,
    SessionKeyUsageSummaryView,
    SessionLogkeyFilterView,
)


urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="user-register"),
    path("login/", LoginUserView.as_view(), name="user-login"),
    path("logout/", LogoutUserView.as_view(), name="user-logout"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("", UsersListCreateAPIView.as_view(), name="users-list-create"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
    path("count/", UsersCountView.as_view(), name="user-count   "),
    path("search/", UsersSearchAPIView.as_view(), name="user-search"),
    path("getall-fullname/", UsersNameList.as_view(), name="user-list-create"),
    path("sessions/", UserSessionCreateView.as_view(), name="create-user-session"),
    path(
        "sessions/update-status/<int:user_id>/",
        SessionStatusUpdateView.as_view(),
        name="session-status-update",
    ),
    path(
        "sessions/regenerate-key/<int:user_id>/",
        SessionKeyRegenerateView.as_view(),
        name="regenerate-session-key",
    ),
    path(
        "sessions/renew-session/<int:user_id>/",
        RenewSessionView.as_view(),
        name="renew-session",
    ),
    path(
        "sessionkey-summary/",
        SessionKeyUsageSummaryView.as_view(),
        name="session-summary-all",
    ),
    path(
        "sessionkey-summary/<int:user_id>/",
        SessionKeyUsageSummaryView.as_view(),
        name="session-summary-user",
    ),
    path("keylogs/", SessionLogkeyFilterView.as_view(), name="session-log-filter"),
    path("getall-endpoints/", EndpointsList.as_view(), name="endpoint-list"),
]
