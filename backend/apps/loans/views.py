from rest_framework import viewsets
from apps.common.permissions import IsBranchManager
from .models import Loan
from .serializers import LoanSerializer

class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [IsBranchManager]