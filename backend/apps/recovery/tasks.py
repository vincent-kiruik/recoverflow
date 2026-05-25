from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum
from apps.recovery.models import RecoveryCase
from apps.collection.models import Collection
from apps.loans.models import Loan


@shared_task
def check_promise_breaches():
    """Escalate cases where promise-to-pay date has passed"""
    today = timezone.now().date()
    breached_cases = RecoveryCase.objects.filter(
        promise_to_pay_date__lt=today,
        status='PROMISE_TO_PAY'
    )
    
    for case in breached_cases:
        case.status = 'ESCALATED'
        case.escalation_level += 1
        case.save()
    
    return f"Escalated {breached_cases.count()} cases"


@shared_task
def send_follow_up_reminders():
    """Daily follow-up reminders"""
    tomorrow = timezone.now().date() + timedelta(days=1)
    cases = RecoveryCase.objects.filter(next_action_date=tomorrow)
    print(f"📧 {cases.count()} cases need follow-up tomorrow")
    return f"Sent reminders for {cases.count()} cases"


@shared_task
def update_loan_aging():
    """Update days overdue for all loans"""
    from django.utils import timezone
    loans = Loan.objects.filter(status__in=['ACTIVE', 'OVERDUE'])
    updated = 0
    for loan in loans:
        if loan.last_repayment_date:
            loan.days_overdue = max(0, (timezone.now().date() - loan.last_repayment_date).days)
            loan.status = 'OVERDUE' if loan.days_overdue > 0 else 'ACTIVE'
            loan.save()
            updated += 1
    return f"Updated aging for {updated} loans"