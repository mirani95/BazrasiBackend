from django.db import models
from apps.authentication import models as auth_models
from apps.core.models import BaseModel


# Create your models here.

class Page(BaseModel):
    """ every front-end page on system """

    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}-{self.code}'

    def save(self, *args, **kwargs):
        super(Page, self).save(*args, **kwargs)


class Permissions(BaseModel):
    """ permission level of users """

    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    category_choices = (
        ('api', 'Api'),
        ('page', 'Page َAccess'),
        ('element', 'UI Element'),
        ('feature', 'Feature / Action')
    )
    category = models.CharField(
        max_length=50,
        choices=category_choices,
        default='api'
    )
    meta = models.JSONField(default=dict)
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        related_name='permission_page',
        null=True
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}-{self.description}'

    def save(self, *args, **kwargs):
        super(Permissions, self).save(*args, **kwargs)


class Role(BaseModel):
    role_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=500)
    type = models.ForeignKey(
        auth_models.OrganizationType,
        on_delete=models.CASCADE,
        related_name="organization_role_type",
        null=True
    )
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return f'{self.role_name}-{self.description}'

    def save(self, *args, **kwargs):
        super(Role, self).save(*args, **kwargs)


class UserRelations(BaseModel):
    user = models.ForeignKey(
        auth_models.User,
        on_delete=models.CASCADE,
        related_name='user_relation',
        null=True
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_role',
        null=True
    )
    permissions = models.ManyToManyField(Permissions)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super(UserRelations, self).save(*args, **kwargs)
