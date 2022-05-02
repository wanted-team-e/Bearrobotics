from django.db import models

# Create your models here.

class Guest(models.Model):
    restuarant = models.ForeignKey()
    created_at = models.DateTimeField()
    price = models.PositiveIntegerField()
    number_of_party = models.PositiveIntegerField()
    payment = models.Charfield()