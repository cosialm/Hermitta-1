from enum import Enum
from datetime import datetime, date # date already imported
from typing import Optional, List, Dict, Any
from decimal import Decimal

# Phase 5: Kenyan Market Localization & Polish (builds on Phase 3 state)
class LeaseSigningStatus(Enum): # From Phase 3
    NOT_STARTED = "NOT_STARTED"
    DRAFT = "DRAFT"
    SENT_FOR_SIGNATURE = "SENT_FOR_SIGNATURE"
    PARTIALLY_SIGNED = "PARTIALLY_SIGNED"
    FULLY_SIGNED_SYSTEM = "FULLY_SIGNED_SYSTEM"
    FULLY_SIGNED_UPLOADED = "FULLY_SIGNED_UPLOADED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    SUPERSEDED = "SUPERSEDED"

class Lease:
    def __init__(self,
                 lease_id: int,
                 property_id: int,
                 landlord_id: int,
                 start_date: date,
                 end_date: date,
                 rent_amount: Decimal,
                 rent_due_day: int,
                 move_in_date: date,
                 tenant_id: Optional[int] = None,
                 tenant_national_id: Optional[str] = None,
                 tenant_name_manual: Optional[str] = None,
                 tenant_phone_number_manual: Optional[str] = None,
                 tenant_email_manual: Optional[str] = None,
                 rent_start_date: Optional[date] = None,
                 security_deposit: Optional[Decimal] = None,
                 notes: Optional[str] = None,
                 lease_document_url: Optional[str] = None,
                 lease_document_version: int = 1,
                 lease_document_uploaded_at: Optional[datetime] = None,
                 lease_document_uploaded_by_user_id: Optional[int] = None,
                 generated_from_template_id: Optional[int] = None,
                 lease_document_content_final: Optional[str] = None,
                 signature_requests: Optional[List[Dict[str, Any]]] = None,
                 signing_status: LeaseSigningStatus = LeaseSigningStatus.NOT_STARTED,
                 signed_lease_document_id: Optional[int] = None,
                 # Phase 5 Refinements:
                 renewal_notice_reminder_date: Optional[date] = None, # Calculated: end_date - notice_period (e.g. 60-90 days)
                 termination_notice_reminder_date: Optional[date] = None, # Calculated for fixed-term end or if notice can be given
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.lease_id = lease_id
        self.property_id = property_id
        self.landlord_id = landlord_id
        self.tenant_id = tenant_id

        self.tenant_national_id = tenant_national_id
        self.tenant_name_manual = tenant_name_manual
        self.tenant_phone_number_manual = tenant_phone_number_manual
        self.tenant_email_manual = tenant_email_manual

        self.start_date = start_date
        self.end_date = end_date
        self.move_in_date = move_in_date
        self.rent_start_date = rent_start_date if rent_start_date is not None else move_in_date

        self.rent_amount = rent_amount
        self.rent_due_day = rent_due_day
        self.security_deposit = security_deposit
        self.notes = notes

        self.lease_document_url = lease_document_url
        self.lease_document_version = lease_document_version
        self.lease_document_uploaded_at = lease_document_uploaded_at
        self.lease_document_uploaded_by_user_id = lease_document_uploaded_by_user_id

        self.generated_from_template_id = generated_from_template_id
        self.lease_document_content_final = lease_document_content_final
        self.signature_requests = signature_requests if signature_requests is not None else []
        self.signing_status = signing_status
        self.signed_lease_document_id = signed_lease_document_id

        # Phase 5 additions
        self.renewal_notice_reminder_date = renewal_notice_reminder_date
        self.termination_notice_reminder_date = termination_notice_reminder_date

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 5):
# from dateutil.relativedelta import relativedelta
# lease_end = date(2025, 12, 31)
# # Assuming a 90-day notice period for renewal as per Kenyan law (example)
# renewal_reminder = lease_end - relativedelta(days=90)
#
# lease_p5 = Lease(
#     lease_id=3, property_id=1, landlord_id=1, tenant_id=201,
#     start_date=date(2024,1,1), end_date=lease_end, rent_amount=Decimal("50000"), rent_due_day=1, move_in_date=date(2024,1,1),
#     signing_status=LeaseSigningStatus.FULLY_SIGNED_SYSTEM,
#     renewal_notice_reminder_date=renewal_reminder
# )
# print(lease_p5.end_date, lease_p5.renewal_notice_reminder_date)
