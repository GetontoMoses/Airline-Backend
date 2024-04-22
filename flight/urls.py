"""urls for the flight app."""

from django.urls import path

from .views import (
   UserLoginView,
   UserSignupView,
   FlightList,
   FlightSearch,
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("flights/", FlightList.as_view(), name="flight_list"),
    path("search/", FlightSearch.as_view(), name="flight_detail"),
]
