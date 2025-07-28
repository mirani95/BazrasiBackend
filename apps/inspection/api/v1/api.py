from rest_framework import viewsets

from apps.inspection.api.v1.serializers import InspectionSerializer
from apps.inspection.models import Inspection


class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.filter(trash=False)
    serializer_class = InspectionSerializer
