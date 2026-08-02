from django.db import models
class ResultStatus(models.TextChoices):
    """
    Result status choices.
    """
    PASS = "PASS", "Pass"
    FAIL = "FAIL", "Fail"
class ResultRecordStatus(models.TextChoices):
    """
    Result record status choices.
    """
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"