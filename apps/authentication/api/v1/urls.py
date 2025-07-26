from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)
from .api import (
    CustomizedTokenObtainPairView,
    UserViewSet,
    CityViewSet,
    ProvinceViewSet,
    OrganizationViewSet,
    OrganizationTypeViewSet,
    GeneralOTPViewSet,
    LogoutView
)

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'city', CityViewSet, basename='city')
router.register(r'province', ProvinceViewSet, basename='province')
router.register(r'organization', OrganizationViewSet, basename='organization')
router.register(r'organization-type', OrganizationTypeViewSet, basename='organization_type')
router.register(r'otp', GeneralOTPViewSet, basename='otp')

urlpatterns = [
    path('login/', CustomizedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logut'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/revoke/', TokenBlacklistView.as_view(), name='revoke_token'),
    path('', include(router.urls))
]
