from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Airline, Airport, Route, Booking
from django.db.models import Q
import random

def flight_list(request):
    airlines = Airline.objects.filter(active="Y")
    return render(request, 'flights/flight_list.html', {'datas': airlines})

def search_flights(request):
    if request.method == "POST":
        initial_destination = request.POST.get('initial_destination')
        final_destination = request.POST.get('final_destination')

    if (not initial_destination or not final_destination):
        return HttpResponse('Give Correct Location in Input')

    else:

        available_routes = Route.objects.filter(
            Q(source_airport_id__in=Airport.objects.filter(
                Q(country=initial_destination) | Q(city=initial_destination))
              .values_list('airport_id', flat=True)) &
            Q(destination_airport_id__in=Airport.objects.filter(
                Q(country=final_destination) | Q(city=final_destination))
              .values_list('airport_id', flat=True))
        )

        return render(request, 'flights/search_results.html', {
            'initial_destination': initial_destination,
            'final_destination': final_destination,
            'datas': available_routes,
        })

@login_required
def flight_detail(request, flight_id):
    route = Route.objects.get(id=flight_id)

    route.available_seats = random.randint(0, 54)
    # A logic to get available seats - Random for now
    return render(request, 'flights/flight_detail.html', {'flight': route})

@login_required
def book_flight(request, flight_id):
    flight = Route.objects.get(id=flight_id)
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        
        existing_booking = Booking.objects.filter(user=request.user, flight=flight).first()
        if existing_booking:
            return render(request, 'flights/book_flight.html', {'flight': existing_booking})
        else:
        
            Booking.objects.create(
                user=request.user,  
                flight=flight,
                seats_booked=seats
            )
            return HttpResponse('booking_success')
