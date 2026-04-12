from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import User, CountryCode
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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




class LoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username', None)  

    def validate(self, attrs):
        email = attrs.get('email')
        phone = attrs.get('phone_number')
        password = attrs.get('password')

        user = None

        if email:
            user = User.objects.filter(email=email).first()
        elif phone:
            user = User.objects.filter(phone_number=phone).first()
        else:
            raise serializers.ValidationError("Email or phone is required")

        if not user or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        refresh = self.get_token(user)

        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }