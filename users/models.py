from django.contrib.auth.models import AbstractUser
from django.db import models

from phone_field import PhoneField

from users.managers import UserManager


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
