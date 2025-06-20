from enum import Enum
from datetime import datetime, date
from typing import Optional, List, Dict, Any
from decimal import Decimal

# Phase 3 Refined (incorporating P5 changes and adding additional_signed_document_ids)
class LeaseSigningStatus(Enum):
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
                 lease_document_url: Optional[str] = None, # URL for the primary unsigned/draft lease document
                 lease_document_version: int = 1,
                 lease_document_uploaded_at: Optional[datetime] = None,
                 lease_document_uploaded_by_user_id: Optional[int] = None,
                 generated_from_template_id: Optional[int] = None,
                 lease_document_content_final: Optional[str] = None, # For in-system signing
                 signature_requests: Optional[List[Dict[str, Any]]] = None,
                 signing_status: LeaseSigningStatus = LeaseSigningStatus.NOT_STARTED,
                 signed_lease_document_id: Optional[int] = None, # FK to Document model for the main signed lease
                 # Phase 3 Refinement: additional signed documents
                 additional_signed_document_ids: Optional[List[int]] = None, # JSON Array of FKs to Document model (e.g., addendums)
                 # Phase 5 Refinements:
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
        self.additional_signed_document_ids = additional_signed_document_ids if additional_signed_document_ids is not None else []

        self.renewal_notice_reminder_date = renewal_notice_reminder_date
        self.termination_notice_reminder_date = termination_notice_reminder_date

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 3 Refined):
# lease_p3_refined = Lease(
#     lease_id=4, property_id=1, landlord_id=1, tenant_id=201,
#     start_date=date(2024,10,1), end_date=date(2025,9,30), rent_amount=Decimal("60000"), rent_due_day=1, move_in_date=date(2024,10,1),
#     signing_status=LeaseSigningStatus.FULLY_SIGNED_UPLOADED,
#     signed_lease_document_id=101, # ID of the main signed lease in Document model
#     additional_signed_document_ids=[102, 103] # IDs of signed addendum 1 and addendum 2
# )
# print(lease_p3_refined.additional_signed_document_ids)
