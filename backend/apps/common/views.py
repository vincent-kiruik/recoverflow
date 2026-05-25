from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from apps.common.permissions import IsBranchManager
from .services.import_service import ArrearsImportService

class ImportViewSet(viewsets.ViewSet):
    permission_classes = [IsBranchManager]
    parser_classes = (MultiPartParser, FormParser)

    @action(detail=False, methods=['post'])
    def arrears(self, request):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        file = request.FILES['file']
        service = ArrearsImportService()
        result = service.import_arrears(file, request.user)

        return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)