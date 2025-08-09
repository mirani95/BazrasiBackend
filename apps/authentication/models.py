from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractUser
)
from django.db import models

from apps.core.models import BaseModel


class User(AbstractUser, BaseModel):
    mobile = models.CharField(max_length=18, null=True)
    phone = models.CharField(max_length=18, null=True)
    national_code = models.CharField(max_length=16, null=True)
    birthdate = models.DateTimeField(null=True)
    nationality = models.CharField(max_length=20, null=True)
    ownership_types = (
        ('N', 'Natural'),
        ('L', 'Legal')
    )
    ownership = models.CharField(
        max_length=1,
        choices=ownership_types,
        default='N',
        help_text="N is natural & L is legal"
    )
    address = models.TextField(max_length=1000, null=True)
    photo = models.CharField(max_length=50, null=True)
    province = models.ForeignKey(
        'Province',
        on_delete=models.CASCADE,
        related_name='user_province',
        null=True
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        related_name='user_city',
        null=True
    )
    otp_status = models.BooleanField(default=False)
    visible_password = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.username} {self.last_name}-{self.last_login}'

    def save(self, *args, **kwargs):
        self.visible_password = self.password
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


class Province(BaseModel):  # noqa
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=250,null=True)
    tel_prefix = models.CharField(max_length=3, null=True)
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Province, self).save(*args, **kwargs)


class City(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=250,null=True)
    province_id = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name='cities',
        null=True
    )
    lat = models.FloatField(default=0)
    lng = models.FloatField(default=0)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(City, self).save(*args, **kwargs)


class OrganizationType(BaseModel):
    organization_keys = (
        ('EMP', 'empty'),
        ('J', 'Jihad'),
        ('U', 'Union'),
        ('CO', 'Cooperative'),
        ('CMP', 'Companies')
    )
    key = models.CharField(choices=organization_keys, default='J', max_length=3)
    name = models.CharField(max_length=50, unique=True, null=True)
    code = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.key}-{self.name}'

    def save(self, *args, **kwargs):
        super(OrganizationType, self).save(*args, **kwargs)


class Organization(BaseModel):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(
        'OrganizationType',
        on_delete=models.CASCADE,
        related_name="organization_type",
        null=True
    )
    national_unique_id = models.CharField(max_length=30, default="0", unique=True)
    activity_fields = (
        ('CO', 'Country'),
        ('PR', 'Province'),
        ('CI', 'City')
    )
    field_of_activity = models.CharField(max_length=2, choices=activity_fields, default="")
    company_code = models.CharField(max_length=30, default="")
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        related_name="province_organization",
        null=True
    )
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        related_name='city_organization',
        null=True
    )
    parent_organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='parents',
        null=True
    )
    additional_data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.name}-{self.type}'

    def save(self, *args, **kwargs):
        super(Organization, self).save(*args, **kwargs)


class OrganizationStats(BaseModel):
    organization = models.OneToOneField(
        Organization,
        on_delete=models.CASCADE,
        related_name='stats',
        null=True
    )
    total_quota_received = models.PositiveBigIntegerField(default=0)
    active_quotas_weight = models.PositiveBigIntegerField(default=0)
    closed_quotas_weight = models.PositiveBigIntegerField(default=0)
    total_quotas_weight = models.PositiveBigIntegerField(default=0)
    total_distributed = models.PositiveBigIntegerField(default=0)
    total_inventory_in = models.PositiveBigIntegerField(default=0)
    total_sold = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return f'Organization: {self.organization.name}'

    def save(self, *args, **kwargs):
        return super(OrganizationStats, self).save(*args, **kwargs)


class BankAccountInformation(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bank_information"
    )
    name = models.CharField(max_length=150)
    card = models.CharField(max_length=25, unique=True)
    account = models.CharField(max_length=25, unique=True)
    sheba = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f'{self.name}-{self.card}'

    def save(self, *args, **kwargs):
        super(BankAccountInformation, self).save(*args, **kwargs)


class BlacklistedAccessToken(models.Model):
    jti = models.CharField(max_length=255, unique=True)
    token = models.TextField()
    user_id = models.IntegerField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted JTI: {self.jti}"
