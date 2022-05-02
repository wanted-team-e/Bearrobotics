from django.contrib import admin

from restaurants.models import Restaurant, Guest, Group, Menu

# Register your models here.

admin.site.register([Restaurant, Guest, Group, Menu])