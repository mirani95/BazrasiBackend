
from rest_framework import serializers
from apps.poultry_inspection.models import PoultryInspection


class PoultryInspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoultryInspection
        fields = '__all__'
