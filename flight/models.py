from django.db import models
from django.contrib.auth.models import User

class Airline(models.Model):
    airline_id = models.IntegerField(primary_key=True)  # Assuming the first number in your CSV is an ID
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255, blank=True, null=True)
    iata = models.CharField(max_length=10, blank=True, null=True)
    icao = models.CharField(max_length=10, blank=True, null=True)
    callsign = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    active = models.CharField(max_length=1)  # Y/N

    def __str__(self):
        return self.name

class Airport(models.Model):
    airport_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    iata = models.CharField(max_length=10, blank=True, null=True)
    icao = models.CharField(max_length=10, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.IntegerField()
    timezone = models.FloatField(blank=True, null=True)
    dst = models.CharField(max_length=10, blank=True, null=True)
    tz_database_time_zone = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    airline = models.ForeignKey('Airline', on_delete=models.CASCADE)
    source_airport = models.ForeignKey(Airport, related_name='outbound_routes', on_delete=models.CASCADE)
    destination_airport = models.ForeignKey(Airport, related_name='inbound_routes', on_delete=models.CASCADE)
    origin = models.CharField(max_length=255, blank=True, null=True)
    destination = models.CharField(max_length=255, blank=True, null=True)
    codeshare = models.CharField(max_length=255, blank=True, null=True)
    stops = models.IntegerField(blank=True, null=True)
    equipment = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.origin:
            source_location = Airport.objects.get(id=self.source_airport_id)
            self.origin = f"{source_location.city}, {source_location.country}"
        
        if not self.destination:
            destination_location = Airport.objects.get(id=self.destination_airport_id)
            self.destination = f"{destination_location.city}, {destination_location.country}"
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.airline} from {self.source_airport} to {self.destination_airport}"


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    available_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.flight_number} from {self.origin} to {self.destination}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
    ]
        
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Route, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    seats_booked = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')


    class Meta:
        unique_together = ('user', 'flight')

    def __str__(self):
        return f"Booking by {self.user.username} for flight {self.flight.id}"