from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.serializers import ClientSerializer, OperatorSerializer
from users.permissions import IsClientPermission, IsOperatorPermission


class BaseUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # User can see only his profile
        if not self.request.user.is_superuser:
            queryset = queryset.filter(id=self.request.user.id)

        return queryset

    def get_permissions(self):
        # Everyone can create new user
        if self.action == "create":
            return [AllowAny()]

        return super().get_permissions()


class ClientViewSet(BaseUserViewSet):
    queryset = User.objects.clients()
    serializer_class = ClientSerializer
    permission_classes = [
        IsClientPermission,
    ] + BaseUserViewSet.permission_classes


class OperatorViewSet(BaseUserViewSet):
    queryset = User.objects.operators()
    serializer_class = OperatorSerializer
    permission_classes = [
        IsOperatorPermission,
    ] + BaseUserViewSet.permission_classes
