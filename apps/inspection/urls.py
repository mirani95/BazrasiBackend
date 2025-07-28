from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.inspection.api.v1.urls'))
]
