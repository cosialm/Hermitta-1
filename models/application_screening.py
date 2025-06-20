from enum import Enum
from datetime import datetime
from typing import Optional

class ScreeningType(Enum):
    CREDIT_CHECK = "CREDIT_CHECK"       # Typically via an integrated service
    BACKGROUND_CHECK = "BACKGROUND_CHECK" # Typically via an integrated service
    MANUAL_REFERENCE_CHECK = "MANUAL_REFERENCE_CHECK" # Landlord calls references
    MANUAL_EMPLOYER_CHECK = "MANUAL_EMPLOYER_CHECK"   # Landlord calls employer
    # EVICTION_HISTORY_CHECK = "EVICTION_HISTORY_CHECK" # Future, if service available

class ScreeningStatus(Enum):
    PENDING_REQUEST = "PENDING_REQUEST"   # Request not yet sent to provider or initiated
    REQUESTED = "REQUESTED"           # Sent to external provider, or initiated for manual check
    IN_PROGRESS = "IN_PROGRESS"         # Provider processing, or landlord actively checking
    COMPLETED_SUCCESS = "COMPLETED_SUCCESS" # Report received, or manual check done, all clear
    COMPLETED_ATTENTION = "COMPLETED_ATTENTION" # Report received or check done, but issues found
    FAILED_TO_OBTAIN = "FAILED_TO_OBTAIN" # Could not get report (e.g., applicant error, provider issue)
    CANCELLED = "CANCELLED"             # Screening request was cancelled by landlord

class ApplicationScreening:
    def __init__(self,
                 screening_id: int,
                 application_id: int, # Foreign Key to RentalApplication
                 screening_type: ScreeningType,
                 status: ScreeningStatus = ScreeningStatus.PENDING_REQUEST,
                 # For manual checks:
                 reference_contact_name: Optional[str] = None,
                 reference_contact_details: Optional[str] = None, # Phone, email
                 screening_notes: Optional[str] = None, # Landlord's notes from manual checks
                 # For integrated checks:
                 provider_name: Optional[str] = None, # e.g., "TransUnion", "Checkr", "Manual"
                 provider_reference_id: Optional[str] = None, # ID from the external provider for this check
                 report_summary: Optional[str] = None, # Brief summary or key findings from provider or manual check
                 screening_report_document_id: Optional[int] = None, # FK to Document model for uploaded report PDF/image
                 requested_at: Optional[datetime] = None, # When the screening was formally requested/initiated
                 completed_at: Optional[datetime] = None, # When the screening was completed
                 updated_at: datetime = datetime.utcnow()):

        self.screening_id = screening_id
        self.application_id = application_id
        self.screening_type = screening_type
        self.status = status

        self.reference_contact_name = reference_contact_name
        self.reference_contact_details = reference_contact_details
        self.screening_notes = screening_notes # Landlord's internal notes for this screening

        self.provider_name = provider_name
        self.provider_reference_id = provider_reference_id
        self.report_summary = report_summary
        self.screening_report_document_id = screening_report_document_id # Link to central Document model

        self.requested_at = requested_at
        self.completed_at = completed_at
        self.updated_at = updated_at

# Example usage:
# credit_check_request = ApplicationScreening(
#     screening_id=1, application_id=101, screening_type=ScreeningType.CREDIT_CHECK,
#     provider_name="CreditSafe Kenya", requested_at=datetime.utcnow(), status=ScreeningStatus.REQUESTED
# )
#
# manual_ref_check = ApplicationScreening(
#     screening_id=2, application_id=101, screening_type=ScreeningType.MANUAL_REFERENCE_CHECK,
#     reference_contact_name="Mr. Previous Landlord", reference_contact_details="0700999888",
#     status=ScreeningStatus.IN_PROGRESS
# )
# # After landlord calls and makes notes:
# # manual_ref_check.screening_notes = "Reference confirmed tenant paid rent on time and kept unit clean."
# # manual_ref_check.status = ScreeningStatus.COMPLETED_SUCCESS
# # manual_ref_check.completed_at = datetime.utcnow()
#
# print(credit_check_request.screening_type, credit_check_request.status)
# print(manual_ref_check.reference_contact_name)
