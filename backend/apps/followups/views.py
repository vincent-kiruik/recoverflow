from rest_framework import viewsets
from apps.common.permissions import IsCollector
from .models import FollowUpAction
from .serializers import FollowUpActionSerializer

class FollowUpActionViewSet(viewsets.ModelViewSet):
    queryset = FollowUpAction.objects.all()
    serializer_class = FollowUpActionSerializer
    permission_classes = [IsCollector]