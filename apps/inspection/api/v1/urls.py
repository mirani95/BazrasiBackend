from rest_framework.routers import DefaultRouter
from django.urls import path, include


router = DefaultRouter()  # set router

# register route to router

urlpatterns = [
    path('', include(router.urls))
]
