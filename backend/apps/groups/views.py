from rest_framework import viewsets
from apps.common.permissions import IsBranchManager

from .models import Group
from .serializers import GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsBranchManager]