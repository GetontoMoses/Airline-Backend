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
            return Response({"access_token": str(access_token), "user_id": user.id})
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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
