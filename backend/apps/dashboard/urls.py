"""
Dashboard URL configuration.
"""
from django.urls import path
from apps.dashboard.views import DashboardAPIView
app_name = "dashboard"
urlpatterns = [
    path(
        "",
        DashboardAPIView.as_view(),
        name="dashboard",
    ),
]