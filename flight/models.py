from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=100)
    destination_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    capacity = models.IntegerField()
    terminal = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Flight {self.flight_number}"


class Booking(models.Model):
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    adults = models.IntegerField(null=True)
    children = models.IntegerField(null=True)
    infants = models.IntegerField(null=True)
    flight_class = models.CharField(max_length=20)
    date_booked = models.DateTimeField(auto_now_add=True)
    Passport_number = models.CharField(max_length=100, null=True)
    Phone_number = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.user} passengers on {self.flight} at {self.date_booked}"
