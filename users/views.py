from rest_framework import viewsets
from .models import User, CountryCode
from .serializers import UserSerializer, CounterCodeSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    