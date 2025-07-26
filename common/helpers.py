import typing
from apps.authorization.models import UserRelations


def detect_file_extension(file_name: str) -> typing.AnyStr:
    """ detect extension of a file like: jpg, png, pdf """
    extended = file_name.split('.')
    return extended[1]


def get_organization_by_user(user: object = None) -> typing.Any:
    organization = UserRelations.objects.select_related('organization').get(user=user).organization
    return organization
