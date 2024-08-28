from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv
from .models import Airline,Airport,Route
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
        
        destination_airport_ids=[]
        source_airport_ids=[]
        airport_mapping={}
        
        source_airport=Airport.objects.filter(Q(country=initial_destination) | Q(city=initial_destination))
        destination_airport=Airport.objects.filter(Q(country=final_destination) | Q(city=final_destination))
        
        with open('flight/static/airports.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                airport_mapping[row['IATA']] = row['Name']
                airport_mapping[row['Name']] = row['City'] +", "+ row['Country']
                if(row['Country']==initial_destination or row['City']==initial_destination):
                    source_airport_ids.append(row['Airport_ID'])
                if(row['Country']==final_destination or row['City']==final_destination):
                    destination_airport_ids.append(row['Airport_ID'])

                    
        available_routes = Route.objects.filter(
            Q(source_airport_id__in=source_airport_ids) &
            Q(destination_airport_id__in=destination_airport_ids))
        
        for index, route in enumerate(available_routes):
            # source_name = airport_mapping.get(route['Source_airport'])
            # source_location = airport_mapping.get(source_name)
            # destination_name = airport_mapping.get(route['Destination_airport'])
            # destination_location = airport_mapping.get(destination_name)
            # route['Source_airport'] = source_name
            # route['Destination_airport'] = destination_name
            # route['source_location']=source_location
            # route['destination_location']=destination_location
            route.route_id=index
            route.available_seats=None

        return render(request, 'flights/search_results.html', {
            'initial_destination': initial_destination,
            'final_destination': final_destination,
            'datas': available_routes,
        })


@login_required
def flight_detail(request, flight_id):
    flight = request.session['value'][flight_id]
    return render(request, 'flights/flight_detail.html', {'flight': flight})

@login_required
def book_flight(request, flight_id):
    flight = request.session['value'][flight_id]
    if request.method == 'POST':
        seats = int(request.POST.get('seats', 1))
        if not flight['available_seats']:
            return HttpResponse('No Available Seats Data Please Contact official Airlines')
        elif seats <= flight['available_seats']:
            flight['seats_booked']=seats
            return HttpResponse('Booking confirmed!')
        else:
            return HttpResponse('Not enough seats available!')
    return render(request, 'flights/book_flight.html', {'flight': flight})
