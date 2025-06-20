from enum import Enum
from datetime import datetime, date
from typing import Optional, Dict, Any
from decimal import Decimal

# Assuming Lease model exists in models.lease
# Assuming User model exists in models.user

class LeaseAmendmentStatus(Enum):
    DRAFT = "DRAFT"                 # Amendment is being prepared, not yet active.
    ACTIVE = "ACTIVE"               # Amendment is active and its terms apply.
    SUPERSEDED = "SUPERSEDED"       # Amendment was active but has been replaced by a newer one.
    CANCELLED = "CANCELLED"         # Amendment was drafted but cancelled before becoming active.
    REJECTED = "REJECTED"           # Amendment proposed but rejected by a party (if workflow included).

class LeaseAmendmentField(Enum): # Enum to standardize field names that can be amended
    RENT_AMOUNT = "rent_amount"
    LEASE_END_DATE = "lease_end_date"
    LEASE_START_DATE = "lease_start_date" # Less common to amend, but possible
    PAYMENT_DAY_OF_MONTH = "payment_day_of_month"
    # Add other specific fields from Lease model that are commonly amended
    TERMS_AND_CONDITIONS_TEXT = "terms_and_conditions_text" # For changes to clauses

class LeaseAmendment:
    def __init__(self,
                 amendment_id: int, # PK
                 lease_id: int, # FK to Lease
                 created_by_user_id: int, # FK to User (who created this amendment)
                 effective_date: date, # Date from which this amendment's changes apply
                 reason: Optional[str] = None, # Reason for the amendment
                 status: LeaseAmendmentStatus = LeaseAmendmentStatus.DRAFT,
                 # Storing changes:
                 # Option 1: A JSON field for all changes. Flexible but less queryable.
                 # changes_json: Optional[Dict[str, Any]] = None,
                 # Option 2: Specific fields for common changes + a JSON field for others.
                 # This provides better structure for common cases.
                 original_rent_amount: Optional[Decimal] = None,
                 new_rent_amount: Optional[Decimal] = None,
                 original_end_date: Optional[date] = None,
                 new_end_date: Optional[date] = None,
                 original_payment_day: Optional[int] = None,
                 new_payment_day: Optional[int] = None,
                 # For more complex changes, like modified clauses or terms:
                 amended_terms_details: Optional[str] = None, # Text describing changes or referencing a document
                 # General field for other changes not fitting above structure
                 other_changes_json: Optional[Dict[str, Any]] = None,
                 # Reference to an uploaded amendment document (optional)
                 amendment_document_id: Optional[int] = None, # FK to Document model
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow(),
                 # Date when the amendment was set to ACTIVE (if applicable)
                 activated_at: Optional[datetime] = None,
                 # User who activated this amendment (if applicable)
                 activated_by_user_id: Optional[int] = None):

        self.amendment_id = amendment_id
        self.lease_id = lease_id
        self.created_by_user_id = created_by_user_id
        self.effective_date = effective_date
        self.reason = reason
        self.status = status

        # Store original and new values for key fields for clarity and history
        self.original_rent_amount = original_rent_amount
        self.new_rent_amount = new_rent_amount
        self.original_end_date = original_end_date
        self.new_end_date = new_end_date
        self.original_payment_day = original_payment_day
        self.new_payment_day = new_payment_day

        self.amended_terms_details = amended_terms_details
        self.other_changes_json = other_changes_json if other_changes_json is not None else {}
        self.amendment_document_id = amendment_document_id

        self.created_at = created_at
        self.updated_at = updated_at
        self.activated_at = activated_at
        self.activated_by_user_id = activated_by_user_id

    # Helper method (conceptual) to apply this amendment to a lease object in memory
    def apply_to_lease(self, lease_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies the amendment's changes to a dictionary representing lease data.
        This is conceptual; actual application logic might be more complex and involve
        persisting changes or recalculating schedules.
        """
        updated_lease_data = lease_data.copy()
        if self.new_rent_amount is not None:
            updated_lease_data['rent_amount'] = self.new_rent_amount
        if self.new_end_date is not None:
            updated_lease_data['end_date'] = self.new_end_date
        if self.new_payment_day is not None:
            updated_lease_data['payment_day_of_month'] = self.new_payment_day
        if self.amended_terms_details is not None:
            # How terms are applied needs careful consideration.
            # This might update a specific field or append to existing terms.
            updated_lease_data['terms_and_conditions_text'] = self.amended_terms_details # Or merge
        if self.other_changes_json:
            for key, value in self.other_changes_json.items():
                updated_lease_data[key] = value
        return updated_lease_data

# Example Usage:
# amendment1 = LeaseAmendment(
#     amendment_id=1,
#     lease_id=101,
#     created_by_user_id=5, # Landlord User ID
#     effective_date=date(2024, 8, 1),
#     reason="Rent increase due to market adjustment.",
#     status=LeaseAmendmentStatus.ACTIVE,
#     original_rent_amount=Decimal("50000.00"),
#     new_rent_amount=Decimal("55000.00"),
#     activated_at=datetime.utcnow(),
#     activated_by_user_id=5
# )
#
# amendment2 = LeaseAmendment(
#     amendment_id=2,
#     lease_id=102,
#     created_by_user_id=5,
#     effective_date=date(2024, 9, 1),
#     reason="Lease extension agreed with tenant.",
#     status=LeaseAmendmentStatus.ACTIVE,
#     original_end_date=date(2024,12,31),
#     new_end_date=date(2025, 6, 30),
#     activated_at=datetime.utcnow(),
#     activated_by_user_id=5
# )
#
# print(amendment1.reason, amendment1.new_rent_amount)
