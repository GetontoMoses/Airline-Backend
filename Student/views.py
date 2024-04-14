"""Student views."""

from django.contrib.auth import authenticate, get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import upload
from .serializers import StudentSerializer, UploadSerializer, UserProfileSerializer

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


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    """View for user profile."""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = "email"


class UploadView(generics.ListCreateAPIView):
    """View for uploading files."""

    parser_classes = [MultiPartParser]
    queryset = upload.objects.all()
    serializer_class = UploadSerializer
    
    def perform_create(self, serializer):
        """Handle file upload logic."""
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        """Overridden to handle file uploads."""

        return self.create(request, *args, **kwargs)


class UploadSearchAPIView(generics.ListCreateAPIView):
    """API view for searching and querying uploaded images."""

    queryset = upload.objects.all()
    serializer_class = UploadSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["name", "year"]


class MyUploads(generics.RetrieveUpdateDestroyAPIView):
    """View for listing user's uploads."""

    queryset = upload.objects.all()
    serializer_class = UploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter uploads by the current user."""
        return upload.objects.filter(user_id=self.request.user.id)
