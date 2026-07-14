from django.apps import AppConfig
class AccountsConfig(AppConfig):
    """
    Configuration for the Accounts application.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts"
