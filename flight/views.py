from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from .models import Airline, Airport, Route
from django.db.models import Q

# url = 'https://opensky-network.org/api/states/all'


def flight_list(request):
    airlines = Airline.objects.filter(active="Y")
    return render(request, 'flights/flight_list.html', {'datas': airlines})


def search_flights(request):
    if request.method == "POST":
        initial_destination = request.POST.get('initial_destination')
        final_destination = request.POST.get('final_destination')

    if (not initial_destination or not final_destination):
        return render(request, 'flights/flight_list.html', {'error': "Give Correct Location in Input"})

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

    source_location = Airport.objects.get(airport_id=route.source_airport_id)
    route.source_location = source_location.city + ', ' + source_location.country

    destination_location = Airport.objects.get(
        airport_id=route.destination_airport_id)
    route.destination_location = destination_location.city + ', ' + destination_location.country

    return render(request, 'flights/flight_detail.html', {'flight': route})


@login_required
def book_flight(request, flight_id):
    flight = Route.objects.get(id=flight_id)
    flight.available_seats = None
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if not flight.available_seats:
            return HttpResponse('No Available Seats Data Please Contact official Airlines')
        elif seats <= flight.available_seats:
            flight.seats_booked=seats
            return HttpResponse('Booking confirmed!')
        else:
            return HttpResponse('Not enough seats available!')
    return render(request, 'flights/book_flight.html', {'flight': flight})
