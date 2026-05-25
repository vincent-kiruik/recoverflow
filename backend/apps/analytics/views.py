from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.common.permissions import IsBranchManager
from .services import DashboardService
from apps.loans.models import Loan


class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        stats = DashboardService.get_dashboard_stats(request.user)
        return Response(stats)

    @action(detail=False, methods=['get'])
    def recovery_trends(self, request):
        trends = DashboardService.get_recovery_trends()
        return Response(trends)

    @action(detail=False, methods=['get'])
    def collector_performance(self, request):
        performance = DashboardService.get_collector_performance()
        return Response(performance)

    @action(detail=False, methods=['get'], url_path='par-analysis')  # Explicit path
    def par_analysis(self, request):
        """Portfolio at Risk (PAR) Analysis"""
        par_data = {
            "par_30": Loan.objects.filter(days_overdue__gte=30, days_overdue__lt=60).count(),
            "par_60": Loan.objects.filter(days_overdue__gte=60, days_overdue__lt=90).count(),
            "par_90": Loan.objects.filter(days_overdue__gte=90).count(),
            "total_overdue": Loan.objects.filter(days_overdue__gt=0).count(),
            "par_30_rate": round(
                Loan.objects.filter(days_overdue__gte=30).count() / 
                (Loan.objects.count() or 1) * 100, 2
            )
        }
        return Response(par_data)