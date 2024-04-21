"""urls for the student app."""

from django.urls import path

from .views import (
    StudentSignUpView,
    UploadView,
    UserLoginView,
    UploadSearchAPIView,
    MyUploadsList,
    MyUploadsCRUD,
)

urlpatterns = [
    path("signup/", StudentSignUpView.as_view(), name="student_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("upload/", UploadView.as_view(), name="upload"),
    path("search/", UploadSearchAPIView.as_view(), name="search"),
    path("myuploads/<int:user>/", MyUploadsList.as_view(), name="myuploads"),
    path("myuploadscrud/<int:pk>/", MyUploadsCRUD.as_view(), name="myuploads"),
]
