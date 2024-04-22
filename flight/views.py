"""flight views."""

from django.contrib.auth import authenticate, get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import Flight
from .serializers import FlightSerializer, UserSerializer


User = get_user_model()


class UserSignupView(generics.CreateAPIView):
    """User signup view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserLoginView(generics.ListCreateAPIView):
    """View for user login."""

    def post(self, request):
        """Handle user login."""
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is not None:
            # User authentication successful, generate JWT token
            access_token = AccessToken.for_user(user)
            return Response(
                {
                    "access_token": str(access_token),
                    "user_id": user.id,
                    "username": user.username,
                }
            )
        else:
            # User authentication failed
            return Response({"error": "Invalid credentials"}, status=401)


class FlightList(generics.ListCreateAPIView):
    """Flight views."""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer


class FlightSearch(generics.ListAPIView):
    """Flight filter."""

    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = [
        "departure_city",
        "destination_city",
        "departure_time",
        "arrival_time",
        "capacity",
        "price",
    ]
