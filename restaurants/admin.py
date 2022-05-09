from django.contrib import admin

from restaurants.models import Restaurant, Guest, Group, Menu

admin.site.register([Restaurant, Guest, Group, Menu])