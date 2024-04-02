"""Student serialzers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import upload

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer."""

    class Meta:
        """Meta class for StudentSerializer."""

        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        """Create a new user."""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class UploadSerializer(serializers.ModelSerializer):
    """Upload serializer."""

    class Meta:
        """Meta class for UploadSerializer."""

        model = upload
        fields = ["name", "image", "year", "uploaded_at"]
