from types import BuiltinFunctionType
from django.db import models
from django.db.models.fields import PositiveIntegerField

# Create your models here.

class Restaurant(models.Model):
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=200, null=False, blank=False)
    restaurant = models.CharField(max_length=200, null=False, blank=False)
    group_id = models.ForeignKey()


class Guest(models.Model):
    restuarant = models.ForeignKey()
    created_at = models.DateTimeField()
    price = models.PositiveIntegerField()
    number_of_party = models.PositiveIntegerField()

    class PaymentType(models.TextChoices):
        CARD = 'CARD'
        CASH = 'CASH'
        BITCOIN = 'BITCOIN'
        PHONE = 'PHONE'
    payment = models.Charfield(
        max_length=20,
        choices=PaymentType.choices
    )

