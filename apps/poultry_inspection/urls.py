from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.poultry_inspection.api.v1.urls'))
]
