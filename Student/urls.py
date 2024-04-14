"""urls for the student app."""

from django.urls import path

from .views import (
    StudentSignUpView,
    UploadView,
    UserLoginView,
    UploadSearchAPIView,
    UserProfileView,
    MyUploads,
)

urlpatterns = [
    path("signup/", StudentSignUpView.as_view(), name="student_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("profile/<str:email>", UserProfileView.as_view(), name="user_profile"),
    path("upload/", UploadView.as_view(), name="upload"),
    path("search/", UploadSearchAPIView.as_view(), name="search"),
    path("myuploads/<int:pk>", MyUploads.as_view(), name="myuploads"),
]
