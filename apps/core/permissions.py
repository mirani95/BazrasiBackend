from rest_framework.permissions import BasePermissionMetaclass
from apps.authorization import models as authorize_models
import itertools
import typing


class BasePermission(metaclass=BasePermissionMetaclass):
    """
    A base class from which all permission classes should inherit.
    """

    def get_user_permissions(self, request, view) -> typing.Dict:  # noqa
        """
        get permissions by role and user specified permissions
        combined permissions and returns a list
        """
        organization_type = []
        permissions_info = {}
        relations = request.user.user_relation.select_related()
        for relation in relations:
            role_permissions = list(itertools.chain(*[
                    list(item.values()) for item in
                    list(relation.role.permissions.prefetch_related().values('name'))
                ]
            ))
            user_permissions = list(itertools.chain(*[
                list(item.values()) for item in
                list(relation.permissions.prefetch_related().values('name'))])
            )
            result = list(set(role_permissions + user_permissions))
            organization_type.append(relation.organization.type.key)
            permissions_info['organization_type'] = organization_type
            permissions_info['permissions'] = result
            print(result, permissions_info)
        return permissions_info

    def has_permission(self, request, view):  # noqa
        """
        Return `True` if permission is granted, `False` otherwise.
        """

        return True

    def has_object_permission(self, request, view, obj):  # noqa
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True
