import typing

from rest_framework import serializers
from apps.authorization.models import (
    Role,
    Permissions,
    UserRelations,
)
from apps.authentication.api.v1.serializers import serializer as auth_serializer
from apps.authentication.models import Organization
import itertools


class PermissionSerializer(serializers.ModelSerializer):
    """ Serialize permissions """

    class Meta:
        model = Permissions
        fields = [
            'id',
            'name',
            'description',
            'category',
            'page',
            'is_active'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['page'] = instance.page.name

        return representation

    @classmethod
    def permissions_structure_output(cls, permissions) -> typing.Any:
        """ set a structure for permissions """

        structure = []
        pages_list = []
        for counter, permission in enumerate(permissions):
            if permission.page.name not in pages_list:
                pages_list.append(permission.page.name)
                structure.append({
                    'page_name': permission.page.name,
                    'page_access': itertools.chain(*list(
                        permissions.filter(page=permission.page).values_list('name')))
                })
        return structure


class RoleSerializer(serializers.ModelSerializer):
    """ Serialize roles of user """

    class Meta:
        model = Role
        fields = [
            'id',
            'role_name',
            'description',
            'type',
            'permissions'
        ]
        extra_kwargs = {
            'permissions': {'required': False}  # permissions not required for some roles
        }

    def to_representation(self, instance):
        """
        using @to_representation for many_to_many permissions in response
        """
        representation = super().to_representation(instance)
        representation['type'] = auth_serializer.OrganizationTypeSerializer(instance.type).data
        if instance.permissions:  # noqa
            permissions = instance.permissions.filter(is_active=True)
            representation['permissions'] = PermissionSerializer(permissions, many=True).data
        return representation


class UserRelationSerializer(serializers.ModelSerializer):
    """ Serialize relations of user like: organizations, roles, permissions """

    class Meta:
        model = UserRelations
        fields = [
            'id',
            'user',
            'role',
            'permissions',
        ]

        extra_kwargs = {
            'permissions': {
                'required': False
            },
            'role': {
                'required': False
            }
        }

    def to_representation(self, instance):
        """ custom output for serializer """

        representation = super().to_representation(instance)
        if isinstance(instance, UserRelations):
            if instance.user:
                representation['user'] = auth_serializer.UserSerializer(instance.user).data
            if instance.role:
                representation['role'] = RoleSerializer(instance.role).data
            if instance.permissions:  # noqa
                # set permissions by a default structure like:
                # 'page permission':[element permissions]
                permissions = instance.permissions.filter(is_active=True)
                representation['permissions'] = PermissionSerializer().permissions_structure_output(permissions)
        return representation

    def update(self, instance, validated_data):
        """ update user relation object """

        instance.role = validated_data.get('role', instance.role)
        instance.save()
        instance.permissions.clear()
        instance.permissions.add(*(validated_data.get('permissions', instance.permissions)))
        return instance
