"""flight views."""

from django.contrib.auth import authenticate, get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import status

from .models import Booking, Flight
from .serializers import BookingSerializer, FlightSerializer, UserSerializer


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


class BookingView(generics.CreateAPIView):
    """Booking view."""
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            flight_id = serializer.validated_data["flight"]
            user_id = serializer.validated_data["user"]

            # Check if a booking with the same flight ID and user ID exists
            existing_booking = Booking.objects.filter(
                flight=flight_id, user=user_id
            ).exists()
            if existing_booking:
                return Response(
                    {"error": "User has already booked this flight"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class bookingInfo(generics.GenericAPIView):
    """Retrieve a booking instance."""

    serializer_class = BookingSerializer
    
    def get(self, request, *args, **kwargs):
        booking = Booking.objects.filter(user=kwargs["user"])
        serialized_bookings = BookingSerializer(booking, many=True)
        return Response(serialized_bookings.data, status=200)

class UserProfile(generics.RetrieveAPIView):
    """User profile view."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        """Retrieve user profile based on user ID."""
        user_id = kwargs.get("pk")
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

class BookingEdit(generics.RetrieveUpdateDestroyAPIView):
    """View for editing a booking."""

    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = Booking.objects.filter(id=self.kwargs["pk"])
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()
