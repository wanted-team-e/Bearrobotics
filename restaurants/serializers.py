from rest_framework import serializers

from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
        editor : 강정희
    """
    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group',
        )
