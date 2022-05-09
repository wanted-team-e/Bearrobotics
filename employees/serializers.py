from rest_framework import serializers

from employees.models import Employee


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'email',
            'password',
            'username',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        email = validated_data['email']
        username = validated_data['username']
        password = validated_data['password']
        user = Employee.objects.create_user(
            email=email,
            username=username,
            password=password
        )
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id',
            'email',
            'password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        email = data.get('email', None)
        user = Employee.objects.filter(email=email).first()
        if user is None:
            return None
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'email',
            'username',
            'rank_type',
        )
        read_only_fields = (
            'email',
        )
