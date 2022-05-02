from django.db import models


# Create your models here.

class Restaurant(models.Model):
    city = models.CharField(max_length=128, null=False, blank=False)
    address = models.CharField(max_length=256)
    restaurant = models.CharField(max_length=256, null=False, blank=False)
    group = models.ForeignKey('restaurants.Group', on_delete=models.CASCADE)


class Guest(models.Model):
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE)
    price = models.PositiveIntegerField(default=0)
    number_of_party = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField()

    class PaymentType(models.TextChoices):
        CARD = 'CARD'
        CASH = 'CASH'
        BITCOIN = 'BITCOIN'
        PHONE = 'PHONE'

    payment = models.CharField(
        max_length=20,
        choices=PaymentType.choices
    )


class Group(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)


class Menu(models.Model):
    group = models.ForeignKey('restaurants.Menu', on_delete=models.CASCADE)
    name = models.CharField(max_length=31)
    price = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name