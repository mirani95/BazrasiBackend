from django.db import models

from apps.authentication import models as auth_models
from common.models import BaseModel


class Inspection(BaseModel):
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
    #todo نوع مالکیت

