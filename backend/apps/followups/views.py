from rest_framework import viewsets
from .models import FollowUpAction
from .serializers import FollowUpActionSerializer

class FollowUpActionViewSet(viewsets.ModelViewSet):
    queryset = FollowUpAction.objects.all()
    serializer_class = FollowUpActionSerializer