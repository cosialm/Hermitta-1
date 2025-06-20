from enum import Enum
from datetime import datetime
from typing import Optional

class ScreeningType(Enum):
    CREDIT_CHECK = "CREDIT_CHECK"
    BACKGROUND_CHECK = "BACKGROUND_CHECK"
    REFERENCE_CHECK = "REFERENCE_CHECK" # Could be manual or automated
    # Add other types as needed, e.g., EVICTION_HISTORY

class ScreeningStatus(Enum):
    PENDING = "PENDING"                 # Request initiated, awaiting processing or report
    IN_PROGRESS = "IN_PROGRESS"           # If the check takes time (e.g., manual reference check)
    COMPLETED = "COMPLETED"             # Screening finished, report/summary available
    FAILED_TO_OBTAIN = "FAILED_TO_OBTAIN" # Could not get the report (e.g., applicant error, provider issue)
    REQUIRES_ATTENTION = "REQUIRES_ATTENTION" # Report received, but needs manual review for flags/issues
    CANCELLED = "CANCELLED"             # Screening request was cancelled

class ApplicationScreening:
    def __init__(self,
                 screening_id: int,
                 application_id: int,
                 screening_type: ScreeningType,
                 status: ScreeningStatus = ScreeningStatus.PENDING,
                 report_summary: Optional[str] = None,
                 report_document_url: Optional[str] = None, # URL to the detailed report (PDF, etc.)
                 requested_at: datetime = datetime.utcnow(),
                 completed_at: Optional[datetime] = None,
                 provider: Optional[str] = None, # e.g., "TransUnion", "Checkr", "Manual"
                 updated_at: datetime = datetime.utcnow()):

        self.screening_id = screening_id
        self.application_id = application_id # Foreign Key to RentalApplication
        self.screening_type = screening_type
        self.status = status
        self.report_summary = report_summary # Brief summary or key findings
        self.report_document_url = report_document_url # Link to the full report
        self.requested_at = requested_at
        self.completed_at = completed_at
        self.provider = provider # Name of the screening service/method
        self.updated_at = updated_at

# Example usage:
# credit_check = ApplicationScreening(
#     screening_id=1, application_id=1, screening_type=ScreeningType.CREDIT_CHECK,
#     provider="ExampleCreditCo"
# )
# print(credit_check.screening_type, credit_check.status)
#
# # After completion:
# # credit_check.status = ScreeningStatus.COMPLETED
# # credit_check.completed_at = datetime.utcnow()
# # credit_check.report_summary = "Credit score: 750. No major issues found."
# # credit_check.report_document_url = "https://example.com/reports/credit_report_app1.pdf"
# # credit_check.updated_at = datetime.utcnow()
