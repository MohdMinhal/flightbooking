from django.contrib import admin
from .models import Airline, Airport, Route, Flight, Booking

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('airline_id', 'name', 'iata', 'icao', 'callsign', 'country', 'active')
    search_fields = ('name', 'iata', 'icao')

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('airport_id', 'name', 'city', 'country', 'iata', 'icao', 'latitude', 'longitude')
    search_fields = ('name', 'iata', 'icao')
    list_filter = ('country',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('airline', 'source_airport', 'destination_airport', 'codeshare', 'stops', 'equipment')
    search_fields = ('airline__name', 'source_airport__name', 'destination_airport__name')
    list_filter = ('airline', 'source_airport', 'destination_airport')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'origin', 'destination', 'departure_time', 'arrival_time', 'available_seats')
    search_fields = ('flight_number', 'origin', 'destination')
    list_filter = ('departure_time', 'arrival_time')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'flight', 'booking_date', 'seats_booked')
    search_fields = ('user__username', 'flight__flight_number')
    list_filter = ('booking_date',)
