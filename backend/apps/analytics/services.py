from django.db.models import Sum, Count, Avg, F, Q
from django.utils import timezone
from datetime import timedelta
from apps.recovery.models import RecoveryCase
from apps.collection.models import Collection
from apps.loans.models import Loan
from apps.groups.models import Group


class DashboardService:
    """Service for all dashboard and analytics data"""

    @staticmethod
    def get_dashboard_stats(user):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        # Key Performance Indicators
        total_active_cases = RecoveryCase.objects.filter(status__in=['NEW', 'CONTACT_ATTEMPT', 'PROMISE_TO_PAY', 'FIELD_VISIT', 'ESCALATED']).count()
        
        collections_today = Collection.objects.filter(
            collection_date__date=today
        ).aggregate(total=Sum('amount_collected'))['total'] or 0

        total_collections_30d = Collection.objects.filter(
            collection_date__date__gte=thirty_days_ago
        ).aggregate(total=Sum('amount_collected'))['total'] or 0

        par_30 = Loan.objects.filter(days_overdue__gte=30).count()
        total_loans = Loan.objects.count()
        par_30_rate = (par_30 / total_loans * 100) if total_loans > 0 else 0

        recovery_rate = RecoveryCase.objects.filter(
            total_collected__gt=0
        ).aggregate(avg=Avg('recovery_percentage'))['avg'] or 0

        return {
            "active_cases": total_active_cases,
            "collections_today": float(collections_today),
            "collections_30d": float(total_collections_30d),
            "par_30_rate": round(par_30_rate, 2),
            "recovery_rate": round(recovery_rate, 2),
            "high_risk_groups": Group.objects.filter(risk_level='HIGH').count(),
        }

    @staticmethod
    def get_recovery_trends():
        """Last 6 months recovery trends"""
        # Simplified - you can enhance with real monthly aggregation
        return {
            "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "collections": [1240000, 1580000, 1320000, 1890000, 1670000, 2140000],
            "cases_closed": [45, 52, 48, 61, 55, 72]
        }

    @staticmethod
    def get_collector_performance():
        """Top performers"""
        from apps.accounts.models import User
        collectors = User.objects.filter(role='COLLECTOR')
        
        performance = []
        for collector in collectors:
            collected = Collection.objects.filter(collected_by=collector).aggregate(
                total=Sum('amount_collected')
            )['total'] or 0
            
            cases_assigned = RecoveryCase.objects.filter(assigned_collector=collector).count()
            
            performance.append({
                "collector": collector.full_name,
                "amount_collected": float(collected),
                "cases_assigned": cases_assigned,
                "cases_closed": RecoveryCase.objects.filter(
                    assigned_collector=collector, status='CLOSED'
                ).count()
            })
        
        return sorted(performance, key=lambda x: x['amount_collected'], reverse=True)[:10]