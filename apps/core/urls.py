from rest_framework.routers import DefaultRouter
from django.urls import path, include

from apps.views import jsdhf

router = DefaultRouter()
app_name = "core"

urlpatterns = [
    path('core/', include(router.urls)),
    path('jsdhf/', jsdhf),
]
