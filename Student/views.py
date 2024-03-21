"""Student views."""

from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import StudentSerializer

User = get_user_model()


class StudentSignUpView(generics.ListCreateAPIView):
    """Create a new student."""

    queryset = User.objects.all()
    serializer_class = StudentSerializer
