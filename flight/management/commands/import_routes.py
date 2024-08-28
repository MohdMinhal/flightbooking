import csv
from django.core.management.base import BaseCommand
from flight.models import Route, Airline, Airport

class Command(BaseCommand):
    help = 'Import routes from routes.dat file into the database'

    def handle(self, *args, **options):
        with open('flight/static/routes.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            routes = [row for row in csv_reader if row['Source_airport_ID'] != '\\N' and row['Destination_airport_ID'] != '\\N' and row['Airline_ID'] != '\\N']
        for row in routes:
            route_data = {
                'airline_id': row['Airline_ID'],
                'source_airport_id': row['Source_airport_ID'],
                'destination_airport_id': row['Destination_airport_ID'],
                'codeshare': row['Codeshare'] if row['Codeshare'] != '\\N' else None,
                'stops': row['Stops'] if row['Stops'] != '\\N' else None,
                'equipment': row['Equipment'] if row['Equipment'] != '\\N' else None,
            }

            try:
                airline = Airline.objects.get(airline_id=route_data['airline_id'])
                source_airport = Airport.objects.get(airport_id=route_data['source_airport_id'])
                destination_airport = Airport.objects.get(airport_id=route_data['destination_airport_id'])

                Route.objects.create(
                    airline=airline,
                    source_airport=source_airport,
                    destination_airport=destination_airport,
                    codeshare=route_data['codeshare'],
                    stops=route_data['stops'],
                    equipment=route_data['equipment']
                )
            except Airline.DoesNotExist:
                self.stdout.write(self.style.ERROR(
                    f"Airline with ID {route_data['airline_id']} not found. Skipping route."))
            except Airport.DoesNotExist as e:
                self.stdout.write(self.style.ERROR(
                    f"Airport not found for ID: {e}. Skipping route."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error creating route with source airport ID {route_data['source_airport_id']} and destination airport ID {route_data['destination_airport_id']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported routes'))
