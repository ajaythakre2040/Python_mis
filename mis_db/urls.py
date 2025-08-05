from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include


def test_view(request):
    return JsonResponse({"message": "Hello from mis app!"})


urlpatterns = [
    path("test/", test_view),
    path("admin/", admin.site.urls),
    path("api/loan/", include("loan.urls")),
    path("api/users/", include("users.urls")),
]
