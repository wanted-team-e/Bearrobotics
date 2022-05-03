import sys
from datetime import datetime
import os
import django
import csv

# system setup
sys.path.append((os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.develop')
django.setup()

from django.conf import settings
from restaurants.models import *

# db upload
base_path = settings.DATA_ROOT_URL + settings.DATA_URL
csv_path = base_path + 'Madup_Wanted_Data_set.csv'

#restaurants.Guest
def insert_guest():
    with open(csv_path, newline = "", encoding = "utf-8") as csvfile:
        data_reader = csv.DictReader(csvfile)

        Guest.objects.all().delete()
        for row in data_reader:
            if row[id]:
                Guest.objects.get_or_create(id = row['id'],
                timestamp = datetime.strptime(row['time']),
                restaurant = row['restaurant'],
                price = int(row['price']),
                number_of_party = int(row['number_of_party']),
                payment = row['payment']
                )
    
    print("Guest CSV UPLOADED SUCCESS!")

insert_guest()