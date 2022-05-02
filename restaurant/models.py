from django.db import models
import uuid

from django.db.models.fields import PositiveIntegerField

# Create your models here.

class Restaurant(models.Model):
    address = models.TextField(max_length=100)
    city = models.CharField(max_length=200, null=False, blank=False)
    restaurant = models.CharField(max_length=200, null=False, blank=False)
    group_id = models.ForeignKey()
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
