from django.db import models


class Flight(models.Model):
    flight_number = models.CharField(max_length=20)
    departure_airport = models.CharField(max_length=100)
    destination_airport = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    duration = models.DurationField()
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"Flight {self.flight_number}"
