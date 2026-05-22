from rest_framework import viewsets
from .models import Borrower
from .serializers import BorrowerSerializer

class BorrowerViewSet(viewsets.ModelViewSet):
    queryset = Borrower.objects.all()
    serializer_class = BorrowerSerializer