import pandas as pd
from django.db import transaction
from django.utils import timezone
from apps.borrowers.models import Borrower
from apps.loans.models import Loan
from apps.recovery.models import RecoveryCase
from apps.groups.models import Group
from uuid import uuid4


class ArrearsImportService:
    """Service to handle Excel arrears import and auto case creation"""

    def __init__(self):
        self.errors = []
        self.success_count = 0
        self.skipped_count = 0

    def import_arrears(self, file_path, user):
        try:
            df = pd.read_excel(file_path)
            
            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        self._process_row(row, user, index + 2)  # +2 for Excel row number
                        self.success_count += 1
                    except Exception as e:
                        self.errors.append(f"Row {index+2}: {str(e)}")
                        self.skipped_count += 1
                        
            return {
                'success': True,
                'imported': self.success_count,
                'skipped': self.skipped_count,
                'errors': self.errors[:50]  # Limit error list
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def _process_row(self, row, user, row_number):
        # Map Excel columns (adjust according to your Excel template)
        client_code = str(row.get('client_code') or row.get('Client Code')).strip()
        full_name = str(row.get('full_name') or row.get('Full Name')).strip()
        national_id = str(row.get('national_id') or row.get('ID Number')).strip()
        loan_number = str(row.get('loan_number') or row.get('Loan Number')).strip()
        outstanding = float(row.get('outstanding_balance') or row.get('Outstanding') or 0)
        days_overdue = int(row.get('days_overdue') or row.get('Days Overdue') or 0)

        # Get or create Borrower
        borrower, _ = Borrower.objects.get_or_create(
            client_code=client_code,
            defaults={
                'full_name': full_name,
                'national_id': national_id,
                'phone_number': row.get('phone') or '',
            }
        )

        # Get or create Loan
        loan, _ = Loan.objects.get_or_create(
            loan_number=loan_number,
            defaults={
                'borrower': borrower,
                'principal_amount': outstanding * 1.2,  # rough estimate
                'outstanding_balance': outstanding,
                'days_overdue': days_overdue,
                'status': 'OVERDUE' if days_overdue > 0 else 'ACTIVE',
                'disbursement_date': timezone.now().date(),
            }
        )

        # Auto-create Recovery Case if overdue
        if days_overdue > 0:
            case_number = f"RC-{timezone.now().strftime('%Y%m%d')}-{str(uuid4())[:8].upper()}"
            
            RecoveryCase.objects.get_or_create(
                loan=loan,
                defaults={
                    'case_number': case_number,
                    'status': 'NEW',
                    'priority': 'HIGH' if days_overdue > 60 else 'MEDIUM',
                    'assigned_collector': user if hasattr(user, 'role') else None,
                }
            )