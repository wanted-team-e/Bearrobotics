import sys
from datetime import datetime
import os
import django
import csv

# system setup
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.develop')
django.setup()

from django.conf import settings
from restaurants.models import Restaurant, Guest, Group

# db upload
base_path = settings.DATA_ROOT_URL + settings.DATA_URL
csv_path1 = base_path + 'Group.csv'
csv_path2 = base_path + 'Restaurant.csv'
csv_path3 = base_path + 'BearRobotics.csv'

#restaurants.Restaurant
def insert_group():
    with open(csv_path1, newline = "", encoding = "utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Group.objects.all().delete()
        for row in data_reader:
            if row['id']:
                Group.objects.get_or_create(id = row['id'],
                name = row['name']),
    print("Group CSV UPLOADED SUCCESS!")

def insert_restaurant():
    with open(csv_path2, newline = "", encoding = "utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Restaurant.objects.all().delete()
        for row in data_reader:
            if row['id']:
                Restaurant.objects.get_or_create(id = row['id'],
                restaurant = row['restaurant'],
                city = row['city'],
                address = row['address'],
                group_id = row['group_id']
                )
    print("Restaurant CSV UPLOADED SUCCESS!")


#restaurants.Guest
def insert_guest():
    with open(csv_path3, newline = "", encoding = "utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Guest.objects.all().delete()
        for row in data_reader:
            if row['id']:
                Guest.objects.get_or_create(id = row['id'],
                timestamp = datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M"),
                restaurant_id = row['restaurant_id'],
                price = int(row['price']),
                number_of_party = int(row['number_of_party']),
                payment = row['payment']
                )
    
    print("Guest CSV UPLOADED SUCCESS!")

insert_group()
insert_restaurant()
insert_guest()