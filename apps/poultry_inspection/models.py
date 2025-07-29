from django.db import models

from apps.authentication import models as auth_models
from apps.core.models import BaseModel
from apps.authentication.models import Province,City


class Poultry(BaseModel):
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='poultry_province',
        null=True
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name='poultry_city',
        null=True
    )
    Lat = models.FloatField(null=True)
    Long = models.FloatField(null=True)
    unit_name = models.CharField(max_length=50, null=True)
    fullname = models.CharField(max_length=250, null=True)
    mobile = models.CharField(max_length=20, null=True)
    breeding_unique_id = models.CharField(max_length=50, null=True)
    quantity = models.BigIntegerField(default=0)
    losses = models.BigIntegerField(default=0)
    left_over = models.BigIntegerField(null=True)
    killed_quantity = models.BigIntegerField(default=0)
    hall = models.IntegerField(default=0)
    date = models.DateTimeField(null=True)
    chicken_breed = models.CharField(max_length=200, null=True)
    period = models.BigIntegerField(default=0, null=True)
    chicken_age = models.IntegerField(default=1)
    total_losses = models.BigIntegerField(default=0)
    licence_number = models.CharField(max_length=20, null=True)
    health_certificate = models.CharField(max_length=100, null=True)
    samasat_discharge_percentage = models.IntegerField(default=0)
    PersonTypeName = models.CharField(max_length=200, null=True, blank=True)
    InteractTypeName = models.CharField(max_length=200, null=True, blank=True)
    UnionTypeName = models.CharField(max_length=200, null=True, blank=True)
    CertId = models.CharField(max_length=200, null=True, blank=True)


class PoultryInspection(BaseModel):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.CASCADE,
        related_name='user_inspection',
        null=True
    )
    business_license = models.CharField(max_length=100, null=True)
    business_license_issuer = models.CharField(max_length=100, null=True)
    licence_number = models.IntegerField(default=0)
    registration_number = models.IntegerField(default=0)
    economic_code = models.IntegerField(default=0)
    type_of_ownership = models.CharField(max_length=250,null=True)
    unit_type = models.CharField(max_length=250,null=True)
    #todo بازرس همراه چیه
    poultry = models.ForeignKey(
        Poultry,
        on_delete=models.CASCADE,
        related_name='poultry_inspection',
        null=True
    )

