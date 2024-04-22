""" flight serializers. """

from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Booking, Flight

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        """Create a new user."""
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user

class FlightSerializer(serializers.ModelSerializer):
    """Flight serializer."""

    class Meta:
        model = Flight
        fields = "__all__"
    
class BookingSerializer(serializers.ModelSerializer):
    """Booking serializer."""

    class Meta:
        model = Booking
        fields = ["id", "flight", "user", "adults", "children", "infants", "flight_class", "date_booked"]