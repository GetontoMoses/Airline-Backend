"""urls for the student app."""

from django.urls import path

from .views import StudentSignUpView, UploadView, UserLoginView

urlpatterns = [
    path("signup/", StudentSignUpView.as_view(), name="student_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("upload/", UploadView.as_view(), name="upload"),
]
