from rest_framework import viewsets

from users.models import User
from users.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = User.objects.clients()
    serializer_class = ClientSerializer
