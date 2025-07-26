from apps.core.models import MobileTest
from rest_framework import serializers


class MobileTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MobileTest
        fields = '__all__'
