from apps.authorization import models as authorize_models
from apps.authentication.models import OrganizationType
from apps.core import permissions


class CreateUser(permissions.BasePermission):
    """
    @permission: superuser can add users
    """

    def has_permission(self, request, view):
        user_level_info = self.get_user_permissions(request, view)
        if 'superuser' in user_level_info['permissions']:
            if 'organization' in request.data.keys():
                org_type = OrganizationType.objects.get(  # noqa
                    id=request.data['organization']['type']
                )
                print(org_type.key)
                if 'J' in user_level_info['organization_type']:
                    return True
                if 'U' in user_level_info['organization_type']:
                    if org_type.key == 'J' or org_type.key == 'U':
                        return False
                    else:
                        return True
                if 'CO' in user_level_info['organization_type']:
                    if org_type.key == 'J' or org_type.key == 'U' or org_type.key == 'CO':
                        return False
                    else:
                        return True
            return True


class CreateOrganization(permissions.BasePermission):
    """
    @permission for adding organization
    """

    def has_permission(self, request, view):
        user_level_info = self.get_user_permissions(request, view)
        if 'superuser' in user_level_info['permissions']:
            org_type = OrganizationType.objects.get(  # noqa
                id=request.data['organization']['type']
            )
            print(org_type.key)
            if 'J' in user_level_info['organization_type']:
                return True
            if 'U' in user_level_info['organization_type']:
                if org_type.key == 'J' or org_type.key == 'U':
                    return False
                else:
                    return True
            if 'CO' in user_level_info['organization_type']:
                if org_type.key == 'J' or org_type.key == 'U' or org_type.key == 'CO':
                    return False
                else:
                    return True
