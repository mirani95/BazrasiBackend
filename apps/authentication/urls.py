from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', '', basename='')

app_name = "authentication"
urlpatterns = [
    path('api/v1/', include('apps.authentication.api.v1.urls')),
]
