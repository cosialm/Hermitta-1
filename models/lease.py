from enum import Enum
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal

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

# New Enum for overall Lease Status
class LeaseStatusType(Enum):
    DRAFT = "DRAFT"                             # Lease is being prepared, not yet active for signing or occupancy
    PENDING_SIGNATURES = "PENDING_SIGNATURES"   # Sent for signature, or signatures being collected
    ACTIVE_PENDING_MOVE_IN = "ACTIVE_PENDING_MOVE_IN" # Signed, tenant has not yet moved in (start_date might be future)
    ACTIVE = "ACTIVE"                           # Lease is current, tenant has moved in or start_date has passed
    EXPIRED_PENDING_RENEWAL = "EXPIRED_PENDING_RENEWAL" # End date passed, awaiting renewal decision/action
    EXPIRED = "EXPIRED"                         # End date passed, tenant moved out or no renewal
    TERMINATED_EARLY = "TERMINATED_EARLY"       # Lease ended before original end_date by agreement or other cause
    CANCELLED = "CANCELLED"                     # Lease was cancelled before it became active (e.g., during draft/pending signature)
    RENEWED = "RENEWED"                         # This specific lease instance has been superseded by a new renewal lease record
    # Note: `signing_status` tracks the e-signature process; `status` tracks overall lifecycle.

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
                 status: LeaseStatusType = LeaseStatusType.DRAFT, # New overall status field
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
                 additional_signed_document_ids: Optional[List[int]] = None,
                 renewal_notice_reminder_date: Optional[date] = None,
                 termination_notice_reminder_date: Optional[date] = None,
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
        self.status = status # Overall lease status
        self.notes = notes

        self.lease_document_url = lease_document_url
        self.lease_document_version = lease_document_version
        self.lease_document_uploaded_at = lease_document_uploaded_at
        self.lease_document_uploaded_by_user_id = lease_document_uploaded_by_user_id

        self.generated_from_template_id = generated_from_template_id
        self.lease_document_content_final = lease_document_content_final
        self.signature_requests = signature_requests if signature_requests is not None else []
        self.signing_status = signing_status # Tracks the e-signature part specifically
        self.signed_lease_document_id = signed_lease_document_id
        self.additional_signed_document_ids = additional_signed_document_ids if additional_signed_document_ids is not None else []

        self.renewal_notice_reminder_date = renewal_notice_reminder_date
        self.termination_notice_reminder_date = termination_notice_reminder_date

        self.created_at = created_at
        self.updated_at = updated_at

# Example:
# lease_active = Lease(..., status=LeaseStatusType.ACTIVE, signing_status=LeaseSigningStatus.FULLY_SIGNED_SYSTEM)
