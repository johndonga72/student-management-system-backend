"""
Reusable abstract base models shared across the project.
"""
from django.db import models
class TimeStampedModel(models.Model):
    """
    Abstract base model that provides timestamp fields.
    """
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date and time when the record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date and time when the record was last updated.",
    )
    class Meta:
        """
        Marks this model as abstract.
        """
        abstract = True
