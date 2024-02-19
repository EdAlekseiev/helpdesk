from django.contrib.auth.models import AbstractUser

from phone_field import PhoneField


class User(AbstractUser):
    phone = PhoneField()
