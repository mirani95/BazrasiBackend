from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.poultry_inspection.api.v1.api import PoultryInspectionViewSet
#
router = DefaultRouter()  # set router
router.register(r'poultry_inspection', PoultryInspectionViewSet, basename='poultry_inspection')

# register route to router
#
urlpatterns = [
    path('', include(router.urls))
]
