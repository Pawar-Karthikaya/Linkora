from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, CountryCode


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'country_code'
        ]

    def validate_phone_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        return value

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_username(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Username must be at least 3 characters long.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

    
class CounterCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCode
        fields = ['id', 'code', 'country_name', 'country_flag']

