"""urls for the flight app."""

from django.urls import path

from .views import (
   BookingEdit,
   UserLoginView,
   UserSignupView,
   FlightList,
   FlightSearch,
   BookingView,
   bookingInfo,
   UserProfile,
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("user/<int:pk>/", UserProfile.as_view(), name="user-profile"),
    path("flights/", FlightList.as_view(), name="flight_list"),
    path("search/", FlightSearch.as_view(), name="flight_detail"),
    path("book/", BookingView.as_view(), name="booking_details"),
    path("booking/<int:user>/", bookingInfo.as_view(), name="booking_details"),
    path("bookingedit/<int:pk>/", BookingEdit.as_view(), name="booking_edit"),
]
