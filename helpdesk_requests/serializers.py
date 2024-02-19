from rest_framework import serializers

from helpdesk_requests.models import Request
from users.models import User
from users.serializers import UserInnerSerializer


class BaseRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            "id",
            "status",
            "body",
            "initiator",
            "processed_by",
        )

    def validate_initiator(self, value: User) -> User:
        """
        User who initiate the request should have Operator group
        """

        if not value.is_client:
            raise serializers.ValidationError(
                "This user can't initiate new request",
            )

        return value

    def validate_processed_by(self, value: User) -> User:
        """
        User who processed the request should have Operator group
        """

        if not value.is_operator:
            raise serializers.ValidationError(
                "This user can't process request",
            )

        return value


class CreateClientRequestSerializer(BaseRequestSerializer):
    class Meta(BaseRequestSerializer.Meta):
        extra_kwargs = {
            "processed_by": {"read_only": True},
            "status": {"read_only": True},
            "initiator": {"read_only": True},
        }


class CreateOperatorRequestSerializer(BaseRequestSerializer):
    class Meta(BaseRequestSerializer.Meta):
        extra_kwargs = {
            "initiator": {"read_only": True},
            "body": {"read_only": True},
        }


class ReadRequestSerializer(BaseRequestSerializer):
    initiator = UserInnerSerializer()
    processed_by = UserInnerSerializer()
