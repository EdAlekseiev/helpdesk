from django.contrib.auth.base_user import BaseUserManager
from django.db.models import QuerySet

from users.utils import constants


class UserManager(BaseUserManager):
    def clients(self) -> QuerySet:
        """
        Returns a queryset of Users with role Client
        """
        return (
            self
            .get_queryset()
            .filter(groups__name=constants.CLIENT_GROUP_NAME)
            .distinct()
        )

    def operators(self) -> QuerySet:
        """
        Returns a queryset of Users with role Operator
        """
        return (
            self
            .get_queryset()
            .filter(groups__name=constants.OPERATOR_GROUP_NAME)
            .distinct()
        )
