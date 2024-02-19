from django.contrib.auth.models import AbstractUser
from django.db import models

from phone_field import PhoneField

from users.managers import UserManager
from users.utils import constants


class User(AbstractUser):
    phone = PhoneField()

    objects = UserManager()

    class Meta(object):
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                name="unique_phone",
            )
        ]

    @property
    def is_operator(self) -> bool:
        """
        Returns True if the user has Operator group
        """
        return self.groups.filter(
            name=constants.OPERATOR_GROUP_NAME,
        ).exists()

    @property
    def is_client(self) -> bool:
        """
        Returns True if the user has Client group
        """
        return self.groups.filter(
            name=constants.CLIENT_GROUP_NAME,
        ).exists()
