"""Student views."""

from django.contrib.auth import authenticate, get_user_model
from django_filters import rest_framework as filters
from rest_framework import generics, permissions
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


class UploadView(generics.CreateAPIView):
    """View for uploading files."""

    queryset = upload.objects.all()
    serializer_class = UploadSerializer

    def post(self, request, *args, **kwargs):
        """Overridden to handle file uploads."""

        return self.create(request, *args, **kwargs)


class UploadSearchAPIView(generics.ListCreateAPIView):
    """API view for searching and querying uploaded images."""

    queryset = upload.objects.all()
    serializer_class = UploadSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ["name", "year"]


class MyUploadsList(generics.GenericAPIView):
    """View for listing all user's uploads."""

    serializer_class = UploadSerializer

    def get(self, request, *args, **kwargs):
        uploads = upload.objects.filter(user=kwargs["user"])
        serialized_uploads = UploadSerializer(uploads, many=True)
        return Response(serialized_uploads.data, status=200)


class MyUploadsCRUD(generics.RetrieveUpdateDestroyAPIView):
    """View for viewing a single upload."""

    serializer_class = UploadSerializer

    def get_queryset(self):
        queryset = upload.objects.filter(id=self.kwargs["pk"])
        return queryset

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response()


class UserProfileView(generics.RetrieveAPIView):
    """View to retrieve a user's profile."""

    serializer_class = StudentSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """Retrieve user profile based on user ID."""
        user_id = kwargs.get("pk")
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)
