from rest_framework import serializers

from restaurants.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    """
        editor : 강정희
    """
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group',
            'group_name',
        )

class TotalPriceDocsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = (
            'name',
        )