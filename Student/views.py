"""Student views."""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import upload
from .serializers import StudentSerializer, UploadSerializer

User = get_user_model()


class StudentSignUpView(generics.ListCreateAPIView):
    """Create a new student."""

    queryset = User.objects.all()
    serializer_class = StudentSerializer


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
            return Response({"access_token": str(access_token)})
        else:
            # User authentication failed
            return Response({"error": "Invalid credentials"}, status=401)


class UploadView(generics.ListCreateAPIView):
    """View for uploading files."""

    parser_classes = [MultiPartParser]
    queryset = upload.objects.all()
    serializer_class = UploadSerializer

    def perform_create(self, serializer):
        """Handle file upload logic."""
        serializer.save()

    def post(self, request, *args, **kwargs):
        """Overridden to handle file uploads."""
        return self.create(request, *args, **kwargs)
