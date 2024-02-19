from django.contrib.auth.base_user import BaseUserManager

from users.utils import constants


class UserManager(BaseUserManager):
    def clients(self):
        return (
            self
            .get_queryset()
            .filter(groups__name=constants.CLIENT_GROUP_NAME)
            .distinct()
        )
