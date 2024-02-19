from django.db.models import QuerySet
from rest_framework import viewsets

from helpdesk.permissions import DjangoModelPermissions
from users.permissions import IsClientPermission, IsOperatorPermission
from helpdesk_requests.models import Request
from helpdesk_requests.serializers import (
    CreateClientRequestSerializer,
    CreateOperatorRequestSerializer,
    ReadRequestSerializer,
)


class BaseRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissions]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReadRequestSerializer

        return super().get_serializer_class()


class ClientRequestViewSet(BaseRequestViewSet):
    """
    Request API endpoint for Request for Client
    """
    queryset = Request.objects.all()
    serializer_class = CreateClientRequestSerializer
    permission_classes = [
        IsClientPermission,
    ] + BaseRequestViewSet.permission_classes

    def get_queryset(self) -> QuerySet:
        """
        Returns the requests of user
        """
        return super().get_queryset().filter(initiator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(initiator=self.request.user)


class OperatorRequestViewSet(BaseRequestViewSet):
    """
    Request API endpoint for Client
    """
    queryset = Request.objects.all()
    serializer_class = CreateOperatorRequestSerializer
    permission_classes = [
        IsOperatorPermission,
    ] + BaseRequestViewSet.permission_classes
