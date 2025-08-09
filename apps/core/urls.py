from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
app_name = "core"

urlpatterns = [
    path('core/', include(router.urls))
]
