"""Student serialzers."""

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class StudentSerializer(serializers.ModelSerializer):
    """Student serializer."""

    class Meta:
        """Meta class for StudentSerializer."""

        model = User
        fields = ["username", "email", "password", "confirm_password"]

    def validate(self, data):
        """Validate the data."""
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("The passwords do not match.")
        return data

    def create(self, validated_data):
        """Create a new user."""
        validated_data.pop("confirm_password", None)
        user = User.objects.create_user(
            username=validated_data["username"], email=validated_data["email"], password=validated_data["password"]
        )
        return user
