"""Accounts app models."""

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class upload(models.Model):
    """Upload model."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="uploads/",)
    year = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return name of the file."""
        return self.name
