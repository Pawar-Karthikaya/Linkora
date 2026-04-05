from rest_framework import viewsets, status, filters
from .models import User, CountryCode
from .serializers import UserSerializer, CounterCodeSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny

class UserViewSet(viewsets.ModelViewSet):
    """
    UserViewSet handles all user-related operations such as:
    - User Registration (create)
    - Listing users (for chat discovery)
    - Searching users (username, email, phone)

    This ViewSet uses Django REST Framework's ModelViewSet,
    which automatically provides CRUD operations.
    """
    queryset = User.objects.all()
    # Serializer defines how User model data is converted
    # between JSON (request/response) and database objects.
    serializer_class = UserSerializer

    # Enables search functionality using DRF's SearchFilter
    # Allows API calls like:
    # GET /users/users/?search=john
    filter_backends = [filters.SearchFilter]

    # Fields on which search will be performed
    search_fields = ['username', 'email', 'phone_number']


    def get_permissions(self):
        """
        Dynamically assign permissions based on action.

        - 'create' action corresponds to user registration.
          This should be accessible to anyone (no authentication required).

        - All other actions (list, retrieve, update, etc.)
          require the user to be authenticated using JWT.
        """
        if self.action == 'create':
            return [AllowAny()]  # Public access for registration
        return [IsAuthenticated()]  # Protected endpoints


    def get_queryset(self):
        """
        Controls which users are returned in API responses.

        - Excludes the currently logged-in user from the list.
        - This is useful for chat systems where a user should
          not see themselves in the user discovery list.

        Example:
        If logged-in user has ID = 1,
        this will return users with ID != 1.
        """
        return User.objects.exclude(id=self.request.user.id)


    def create(self, request, *args, **kwargs):
        """
        Handles user registration.

        Flow:
        1. Validate incoming request data using serializer
        2. If validation fails → return structured error response
        3. If valid → save user (password hashing handled in serializer)
        4. Return custom success response

        Custom response format is used instead of default DRF response
        for better frontend integration and consistency.
        """

        # Deserialize and validate input data
        serializer = self.get_serializer(data=request.data)

        # If validation fails, return error response
        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "error": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save user to database
        # Note: password hashing should be handled in serializer's create()
        serializer.save()

        # Return success response with created user data
        return Response(
            {
                "success": True,
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class LoginView(TokenObtainPairView):
     serializer_class = LoginSerializer


class CountryCodeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CountryCode.objects.all()
    serializer_class = CounterCodeSerializer