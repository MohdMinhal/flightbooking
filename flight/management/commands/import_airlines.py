import csv
from django.core.management.base import BaseCommand
from flight.models import Airline

class Command(BaseCommand):
    help = 'Import airlines from a CSV file into the database'

    def handle(self, *args, **kwargs):
        with open('flight/static/airlines.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                if not Airline.objects.filter(airline_id=int(row['Airline_ID'])).exists():
                    Airline.objects.create(
                        airline_id=int(row['Airline_ID']),
                        name=row['Name'],
                        alias=row['Alias'] if row['Alias'] != '\\N' else None,
                        iata=row['IATA'] if row['IATA'] != '\\N' else None,
                        icao=row['ICAO'] if row['ICAO'] != '\\N' else None,
                        callsign=row['Callsign'] if row['Callsign'] != '\\N' else None,
                        country=row['Country'] if row['Country'] != '\\N' else None,
                        active=row['Active']
                    )
