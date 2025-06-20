from enum import Enum
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

class QuoteStatus(Enum):
    DRAFT = "DRAFT"             # Vendor is preparing the quote
    SUBMITTED = "SUBMITTED"       # Vendor submitted to Landlord
    VIEWED_BY_LANDLORD = "VIEWED_BY_LANDLORD" # Landlord has seen the quote
    APPROVED = "APPROVED"         # Landlord approved
    REJECTED = "REJECTED"         # Landlord rejected
    EXPIRED = "EXPIRED"           # Quote validity period passed
    SUPERSEDED = "SUPERSEDED"     # A new quote has replaced this one
    CANCELLED_BY_VENDOR = "CANCELLED_BY_VENDOR" # Vendor withdrew the quote

class Quote:
    def __init__(self,
                 quote_id: int,
                 maintenance_request_id: int, # Foreign Key to MaintenanceRequest
                 vendor_user_id: int, # Foreign Key to User (with VENDOR role)
                 landlord_user_id: int, # Foreign Key to User (Landlord associated with the property/request)
                 amount: Decimal,       # Total quoted amount
                 description_of_work: str, # Detailed scope of work for this quote
                 valid_until: Optional[date] = None, # Date until which the quote is valid
                 status: QuoteStatus = QuoteStatus.DRAFT,
                 submitted_at: Optional[datetime] = None, # Set when vendor submits
                 approved_or_rejected_at: Optional[datetime] = None,
                 landlord_comments: Optional[str] = None, # Landlord's comments on approval/rejection
                 vendor_comments: Optional[str] = None, # Vendor's initial comments/notes with the quote
                 quote_document_id: Optional[int] = None, # FK to Document model for an uploaded PDF quote
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.quote_id = quote_id
        self.maintenance_request_id = maintenance_request_id
        self.vendor_user_id = vendor_user_id
        self.landlord_user_id = landlord_user_id # Important for linking who approves

        self.amount = amount
        self.description_of_work = description_of_work
        self.valid_until = valid_until
        self.status = status

        self.submitted_at = submitted_at
        self.approved_or_rejected_at = approved_or_rejected_at
        self.landlord_comments = landlord_comments
        self.vendor_comments = vendor_comments
        self.quote_document_id = quote_document_id # Link to an uploaded document

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# plumbing_quote = Quote(
#     quote_id=1, maintenance_request_id=501, vendor_user_id=301, landlord_user_id=10,
#     amount=Decimal("2500.00"),
#     description_of_work="Replace kitchen tap, including all parts and labor for fixing the leak.",
#     valid_until=date(2024, 4, 15),
#     status=QuoteStatus.SUBMITTED,
#     submitted_at=datetime.utcnow(),
#     vendor_comments="Includes high-quality ceramic tap."
# )
#
# # After landlord approval:
# # plumbing_quote.status = QuoteStatus.APPROVED
# # plumbing_quote.approved_or_rejected_at = datetime.utcnow()
# # plumbing_quote.landlord_comments = "Approved. Please proceed ASAP."
#
# print(plumbing_quote.maintenance_request_id, plumbing_quote.amount, plumbing_quote.status)
