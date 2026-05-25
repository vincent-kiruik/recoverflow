from rest_framework import viewsets
from .models import Collection
from .serializers import CollectionSerializer
from apps.common.permissions import IsCollector

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [IsCollector]