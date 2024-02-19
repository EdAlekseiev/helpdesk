from rest_framework import viewsets

from users.models import User
from users.serializers import OperatorSerializer


class OperatorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.operators()
    serializer_class = OperatorSerializer
