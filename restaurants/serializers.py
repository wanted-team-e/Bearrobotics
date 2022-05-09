from rest_framework import serializers
from restaurants.models import Restaurant, Guest, Group, Menu


class RestaurantCUDSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """

    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group',
        )


class RestaurantRSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    group_name = serializers.ReadOnlyField(source='group.name')

    class Meta:
        model = Restaurant
        fields = (
            'name',
            'city',
            'address',
            'group_name',
        )


class TotalPriceDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    timeunit = serializers.CharField()
    total_price = serializers.IntegerField()

    class Meta:
        model = Guest
        fields = (
            'timeunit',
            'restaurant',
            'total_price',
        )


class PaymentDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    timeunit = serializers.CharField()
    count = serializers.IntegerField()

    class Meta:
        model = Guest
        fields = (
            'timeunit',
            'restaurant',
            'payment',
            'count',
        )


class PartyDocsSerializer(serializers.ModelSerializer):
    """
        작성자 : 김채욱
    """
    timeunit = serializers.CharField()
    count = serializers.IntegerField()
    restaurant_id = serializers.IntegerField()

    class Meta:
        model = Guest
        fields = (
            'number_of_party',
            'timeunit',
            'restaurant_id',
            'count',
        )


class GuestCUDSerializer(serializers.ModelSerializer):
    """
        작성자 : 서재환
    """

    class Meta:
        model = Guest
        fields = (
            'restaurant',
            'price',
            'number_of_party',
            'timestamp',
            'payment'
        )

        read_only_fields = (
            'group',
        )


class GuestRSerializer(serializers.ModelSerializer):
    """
        작성자 : 강정희
    """
    restaurant_name = serializers.ReadOnlyField(source='restaurant.name')

    class Meta:
        model = Guest
        fields = (
            'restaurant_name',
            'price',
            'number_of_party',
            'timestamp',
            'payment'
        )


class GroupSerializer(serializers.ModelSerializer):
    """
        editor : 서재환
    """

    class Meta:
        model = Group
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            'group',
            'name',
            'price',
            'created_at',
            'updated_at',
        )