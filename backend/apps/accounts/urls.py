"""
URL configuration for the accounts module.
This module defines all API endpoints related to
authentication and user accounts.
"""
from django.urls import path
from apps.accounts.views import (
    LoginAPIView,
    RegisterAPIView,
    ProfileAPIView,
)
app_name = "accounts"
urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="register"),
    path("auth/login/", LoginAPIView.as_view(), name="login"),
     path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),
]