"""
Production settings for the Student Management System.

These settings are used in the production environment.
"""
from .base import *
# ==========================================================
# Security
# ==========================================================
SECRET_KEY = 'django-insecure--(&3+h&s_^rv03(x7&l*uze9l$p8)!)u8-9w3+-5oi20vrwidj'
DEBUG = False
ALLOWED_HOSTS = [
    "your-domain.com",
]
# ==========================================================
# Database
# ==========================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# ==========================================================
# Security Settings
# ==========================================================
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
