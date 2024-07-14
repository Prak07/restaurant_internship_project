import csv
import json
import os
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurant_assignment.settings")
django.setup()

from restaurant.models import Restaurant

def import_restaurants(csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            try:
                full_details = json.loads(row['full_details'])
            except json.JSONDecodeError as e:
                full_details = {}
            try:
                items = json.loads(row['items'])
            except json.JSONDecodeError as e:
                continue
            restaurant = Restaurant(
                id=row["id"],
                name=row['name'],
                location=row['location'],
                items = items,
                latitude=float(row['lat_long'].split(',')[0]),
                longitude=float(row['lat_long'].split(',')[1]),
                full_details=full_details
            )
            restaurant.save()

import_restaurants('restaurants_small.csv')