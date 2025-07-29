from rest_framework import viewsets

from apps.poultry_inspection.api.v1.serializers import PoultryInspectionSerializer
from apps.poultry_inspection.models import PoultryInspection


class PoultryInspectionViewSet(viewsets.ModelViewSet):
    queryset = PoultryInspection.objects.filter(trash=False)
    serializer_class = PoultryInspectionSerializer
