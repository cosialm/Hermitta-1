from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal # For application_fee_amount

class RentalApplicationStatus(Enum):
    DRAFT = "DRAFT"             # Applicant started but not yet submitted
    SUBMITTED = "SUBMITTED"       # Applicant submitted, pending review
    UNDER_REVIEW = "UNDER_REVIEW" # Landlord is actively reviewing
    AWAITING_DOCUMENTS = "AWAITING_DOCUMENTS" # Waiting for applicant to upload required docs
    AWAITING_FEE_PAYMENT = "AWAITING_FEE_PAYMENT" # Waiting for application fee
    APPROVED = "APPROVED"         # Application approved
    REJECTED = "REJECTED"         # Application rejected
    WITHDRAWN = "WITHDRAWN"       # Applicant withdrew their application
    EXPIRED = "EXPIRED"           # Application expired due to inactivity or time limit

class ApplicationFeeStatus(Enum):
    NOT_APPLICABLE = "NOT_APPLICABLE" # No fee required
    PENDING = "PENDING"               # Fee is due
    PAID = "PAID"                     # Fee has been paid
    WAIVED = "WAIVED"                 # Fee was waived by landlord

class RentalApplication:
    def __init__(self,
                 application_id: int,
                 property_id: int,
                 # Basic applicant info (can be pre-filled if applicant is an existing User)
                 full_name: str,
                 email: str,
                 phone_number: str,
                 applicant_user_id: Optional[int] = None, # FK to User, if applicant is existing user
                 # Standard application data (could be a JSON field or specific columns)
                 application_data: Optional[Dict[str, Any]] = None, # Main structured data from applicant
                 custom_fields_data: Optional[Dict[str, Any]] = None, # For landlord-defined questions/answers (Phase 3 refinement)

                 status: RentalApplicationStatus = RentalApplicationStatus.DRAFT, # Default to DRAFT
                 submitted_at: Optional[datetime] = None, # Set when applicant hits submit
                 reviewed_at: Optional[datetime] = None,
                 notes_for_landlord: Optional[str] = None, # By applicant
                 internal_notes: Optional[str] = None, # By landlord for internal review

                 # Consent flags (Phase 3 refinement)
                 applicant_consent_data_processing: bool = False,
                 applicant_consent_background_check: bool = False,

                 # Application Fee (Phase 3 refinement)
                 application_fee_amount: Optional[Decimal] = None, # Amount if applicable
                 application_fee_paid_status: ApplicationFeeStatus = ApplicationFeeStatus.NOT_APPLICABLE,
                 # payment_id for application fee if integrated with Payment model could be added later
                 # application_fee_payment_id: Optional[int] = None,

                 created_at: datetime = datetime.utcnow(), # When the application record was initiated
                 updated_at: datetime = datetime.utcnow()
                ):

        self.application_id = application_id
        self.property_id = property_id
        self.applicant_user_id = applicant_user_id

        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number

        self.application_data = application_data if application_data is not None else {}
        self.custom_fields_data = custom_fields_data if custom_fields_data is not None else {}

        self.status = status
        if status == RentalApplicationStatus.SUBMITTED and submitted_at is None: # Auto-set submitted_at if status is SUBMITTED
            self.submitted_at = datetime.utcnow()
        else:
            self.submitted_at = submitted_at

        self.reviewed_at = reviewed_at
        self.notes_for_landlord = notes_for_landlord
        self.internal_notes = internal_notes

        self.applicant_consent_data_processing = applicant_consent_data_processing
        self.applicant_consent_background_check = applicant_consent_background_check

        self.application_fee_amount = application_fee_amount
        self.application_fee_paid_status = application_fee_paid_status

        self.created_at = created_at
        self.updated_at = updated_at

# Example usage:
# app_data_example = { "monthly_income": 50000, "current_employer": "Big Corp", "years_at_employer": 3 }
# custom_data_example = { "reason_for_moving": "Closer to work", "number_of_pets": 0 }
#
# application1 = RentalApplication(
#     application_id=1, property_id=101, full_name="Alice Applicant",
#     email="alice@example.com", phone_number="0712345001", applicant_user_id=201,
#     application_data=app_data_example, custom_fields_data=custom_data_example,
#     applicant_consent_data_processing=True, applicant_consent_background_check=True,
#     application_fee_amount=Decimal("50.00"),
#     application_fee_paid_status=ApplicationFeeStatus.PENDING,
#     status=RentalApplicationStatus.SUBMITTED # This will auto-set submitted_at
# )
# print(application1.full_name, application1.status, application1.custom_fields_data.get("reason_for_moving"))
