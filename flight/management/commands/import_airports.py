import csv
from django.core.management.base import BaseCommand
from flight.models import Airport

class Command(BaseCommand):
    help = 'Import airports data from a CSV file'

    def handle(self, *args, **kwargs):
        with open('flight/static/airports.dat', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                airport_data = {
                    'airport_id': int(row['Airport_ID']),
                    'name': row['Name'] if row['Name'] != '\\N' else None,
                    'city': row['City'] if row['City'] != '\\N' else None,
                    'country': row['Country'] if row['Country'] != '\\N' else None,
                    'iata': row['IATA'] if row['IATA'] != '\\N' else None,
                    'icao': row['ICAO'] if row['ICAO'] != '\\N' else None,
                    'latitude': float(row['Latitude']) if row['Latitude'] != '\\N' else None,
                    'longitude': float(row['Longitude']) if row['Longitude'] != '\\N' else None,
                    'altitude': int(row['Altitude']) if row['Altitude'] != '\\N' else None,
                    'timezone': float(row['Timezone']) if row['Timezone'] != '\\N' else None,
                    'dst': row['DST'] if row['DST'] != '\\N' else None,
                    'tz_database_time_zone': row['Tz database time zone'] if row['Tz database time zone'] != '\\N' else None,
                    'type': row['Type'] if row['Type'] != '\\N' else None,
                    'source': row['Source'] if row['Source'] != '\\N' else None,
                }

                _, created = Airport.objects.update_or_create(
                    airport_id=airport_data['airport_id'],
                    defaults=airport_data
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported airports data'))
