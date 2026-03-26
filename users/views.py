from rest_framework import viewsets, status
from .models import User, CountryCode
from .serializers import UserSerializer, CounterCodeSerializer
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "error": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
        serializer.save()
        return Response(
            {
                "sucsess": True,
                "Data": serializer.data
            },
            status.HTTP_201_CREATED    
        )