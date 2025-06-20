from datetime import datetime, date
from typing import Optional
from decimal import Decimal # For currency values

# Phase 2: Enhanced for document versioning
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
                 # Lease Document Fields (enhanced for Phase 2)
                 lease_document_url: Optional[str] = None, # URL for the current/latest lease document
                 lease_document_version: int = 1, # Starts at 1, increments on new uploads
                 lease_document_uploaded_at: Optional[datetime] = None, # Timestamp of last upload
                 lease_document_uploaded_by_user_id: Optional[int] = None, # FK to User who uploaded
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

        # Lease Document details
        self.lease_document_url = lease_document_url # Replaces initial_scanned_lease_document_url
        self.lease_document_version = lease_document_version
        self.lease_document_uploaded_at = lease_document_uploaded_at
        self.lease_document_uploaded_by_user_id = lease_document_uploaded_by_user_id

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 2):
# lease1 = Lease(
#     lease_id=1, property_id=1, landlord_id=1,
#     start_date=date(2024, 7, 1), end_date=date(2025, 6, 30),
#     move_in_date=date(2024, 7, 5),
#     rent_amount=Decimal("25000.00"), rent_due_day=5,
#     tenant_name_manual="Alice Tenant", tenant_national_id="87654321",
#     lease_document_url="https://example.com/leases/lease_alice_v1.pdf",
#     lease_document_version=1,
#     lease_document_uploaded_at=datetime.now(),
#     lease_document_uploaded_by_user_id=1 # Landlord uploaded
# )
#
# # After an addendum or re-upload:
# # lease1.lease_document_url = "https://example.com/leases/lease_alice_v2.pdf"
# # lease1.lease_document_version = 2
# # lease1.lease_document_uploaded_at = datetime.now()
# # lease1.lease_document_uploaded_by_user_id = 1
# # lease1.updated_at = datetime.now()
#
# print(lease1.tenant_name_manual, lease1.lease_document_url, lease1.lease_document_version)
