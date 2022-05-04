from django.contrib.auth import authenticate
from rest_framework import serializers

from employees.models import Employee


class AuthenticationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'email',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

        def validate(self, data):
            email = data.get('email')
            password = data.get('password')

            employee = authenticate(email=email, password=password)

            if employee is None:
                return None
            return employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'email',
            'username',
            'rank',
            'group',
        )