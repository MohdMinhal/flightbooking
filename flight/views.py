from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import csv

# url = 'https://opensky-network.org/api/states/all'

def flight_list(request):
    with open('flight/static/airlines.dat', 'r') as file:
        csv_reader = csv.DictReader(file)
        airlines = [row for row in csv_reader if (row['Active'] == "Y")]
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
        available_routes=[]
        airport_mapping={}
        airline_mapping={}
        
        with open('flight/static/airports.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                airport_mapping[row['IATA']] = row['Name']
                airport_mapping[row['Name']] = row['City'] +", "+ row['Country']
                if(row['Country']==initial_destination or row['City']==initial_destination):
                    source_airport_ids.append(row['Airport_ID'])
                if(row['Country']==final_destination or row['City']==final_destination):
                    destination_airport_ids.append(row['Airport_ID'])

        with open('flight/static/routes.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if(row['Source_airport_ID'] in source_airport_ids and row['Destination_airport_ID'] in destination_airport_ids):
                    available_routes.append(row)
                    
        with open('flight/static/airlines.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                airline_mapping[row['Airline_ID']] = row['Name']
        
        for index, route in enumerate(available_routes):
            airline_name= airline_mapping.get(route['Airline_ID'])
            source_name = airport_mapping.get(route['Source_airport'])
            source_location = airport_mapping.get(source_name)
            destination_name = airport_mapping.get(route['Destination_airport'])
            destination_location = airport_mapping.get(destination_name)
            route['Airline']=airline_name
            route['Source_airport'] = source_name
            route['Destination_airport'] = destination_name
            route['source_location']=source_location
            route['destination_location']=destination_location
            route['Route_id']=index
            route['available_seats']=None
        
        request.session['value']=available_routes
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
