from django.urls import path

from apps.examinations.views import (
    ExaminationAPIView,
    ExaminationDeleteAPIView,
    ExaminationListAPIView,
    ExaminationStatusAPIView,
)

urlpatterns = [
    path(
        "",
        ExaminationListAPIView.as_view(),
        name="examination-list",
    ),
    path(
        "create/",
        ExaminationAPIView.as_view(),
        name="examination-create",
    ),
    path(
        "<int:examination_id>/",
        ExaminationAPIView.as_view(),
        name="examination-detail",
    ),
    path(
        "<int:examination_id>/status/",
        ExaminationStatusAPIView.as_view(),
        name="examination-status",
    ),
    path(
        "<int:examination_id>/delete/",
        ExaminationDeleteAPIView.as_view(),
        name="examination-delete",
    ),
]