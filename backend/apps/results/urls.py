"""
Result URL configuration.
"""
from django.urls import path
from apps.results.views import (
    ResultAPIView,
    ResultDeleteAPIView,
    ResultListAPIView,
    ResultStatusAPIView,
)
urlpatterns = [
    path(
        "",
        ResultListAPIView.as_view(),
        name="result-list",
    ),
    path(
        "create/",
        ResultAPIView.as_view(),
        name="result-create",
    ),
    path(
        "<int:result_id>/",
        ResultAPIView.as_view(),
        name="result-detail",
    ),
    path(
        "<int:result_id>/update/",
        ResultAPIView.as_view(),
        name="result-update",
    ),
    path(
        "<int:result_id>/status/",
        ResultStatusAPIView.as_view(),
        name="result-status",
    ),
    path(
        "<int:result_id>/delete/",
        ResultDeleteAPIView.as_view(),
        name="result-delete",
    ),
]