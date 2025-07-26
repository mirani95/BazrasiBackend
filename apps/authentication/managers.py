from django.db import models
from typing import Any
from apps.authentication import models as authentication_models
from apps.authorization import models as authorization_models


class UserManager(models.Manager):

    @staticmethod
    def get_user_information(self, user_id: int) -> Any:
        """ get user information in 3 models and return 3 objects """
        user = super().get_queryset().get(id=user_id)
        yield user
        bank = authentication_models.BankAccountInformation.objects.get(user_id=user_id)
        yield bank
        user_relation = authorization_models.objects.get(user_id=user_id)
        yield user_relation

