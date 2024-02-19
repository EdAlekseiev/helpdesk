from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from users.utils import constants


class OperatorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {
                "required": True,
                "validators": [
                    UniqueValidator(queryset=User.objects.all())
                ]
            },
        }

    def create(self, validated_data):
        operator = super().create(validated_data)
        # Add group Operator to user
        operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)
        operator.groups.add(operator_group)

        return operator
