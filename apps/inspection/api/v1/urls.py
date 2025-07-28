from rest_framework.routers import DefaultRouter
from django.urls import path, include
from apps.inspection.api.v1.api import InspectionViewSet

router = DefaultRouter()  # set router
router.register(r'inspection', InspectionViewSet, basename='inspection')

# register route to router

urlpatterns = [
    path('', include(router.urls))
]
