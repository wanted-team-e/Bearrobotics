from rest_framework import serializers

from restaurants.models import Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = (
            'restaurant',
            'price',
            'number_of_party',
            'timestamp',
            'payment'
        )