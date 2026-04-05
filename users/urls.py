from django.urls import path, include
from .views import UserViewSet, LoginView, CountryCodeViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('countrycode/', CountryCodeViewSet.as_view({'get': 'list'}), name='countrycode')
]
