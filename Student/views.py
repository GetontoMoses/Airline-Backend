"""Student views."""

from rest_framework import generics

from django.contrib.auth import get_user_model

from .serializers import StudentSerializer

User = get_user_model()


class StudentSignUpView(generics.ListCreateAPIView):
    """Create a new student."""

    queryset = User.objects.all()
    serializer_class = StudentSerializer
