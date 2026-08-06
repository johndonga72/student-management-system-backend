"""
Development settings for the Student Management System.

These settings are used during local development.
"""

from .base import *
# ==========================================================
# Security
# ==========================================================

SECRET_KEY = "django-insecure--(&3+h&s_^rv03(x7&l*uze9l$p8)!)u8-9w3+-5oi20vrwidj"

DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

# ==========================================================
# Database
# ==========================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "student_erp_db",
        "USER": "postgres",
        "PASSWORD": "john144",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# ==========================================================
# Email Backend
# ==========================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"