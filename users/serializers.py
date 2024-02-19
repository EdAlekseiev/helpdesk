import logging

from django.contrib.auth.models import Group

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from users.utils import constants, otp


logger = logging.getLogger(__name__)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "phone": {
                "required": True,
                "validators": [
                    UniqueValidator(queryset=User.objects.all())
                ]
            },
        }

    def validate(self, data):
        data = super().validate(data)

        # We should provide username as phone and temporary password
        # in order client can log in our system
        data["username"] = data["phone"]
        otp_code = otp.generate_otp()
        data["password"] = otp_code
        logger.debug(f"OTP Code for {data['phone']}: {otp_code}")

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        client = super().create(validated_data)
        # Add group Client to user
        client_group = Group.objects.get(name=constants.CLIENT_GROUP_NAME)
        client.groups.add(client_group)
        client.set_password(password)
        client.save()

        return client


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
        password = validated_data.pop("password")
        operator = super().create(validated_data)
        # Add group Operator to user
        operator_group = Group.objects.get(name=constants.OPERATOR_GROUP_NAME)
        operator.groups.add(operator_group)
        operator.set_password(password)

        return operator


class UserInnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
        )
