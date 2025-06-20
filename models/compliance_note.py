from enum import Enum
from datetime import datetime, date # Added date
from typing import Optional, List # Added List

class ComplianceArea(Enum):
    # Data Protection Act, 2019
    DPA_GENERAL_PRINCIPLES = "DPA_GENERAL_PRINCIPLES"
    DPA_CONSENT_MANAGEMENT = "DPA_CONSENT_MANAGEMENT"
    DPA_DATA_SUBJECT_RIGHTS_ACCESS = "DPA_DATA_SUBJECT_RIGHTS_ACCESS"
    DPA_DATA_SUBJECT_RIGHTS_RECTIFICATION = "DPA_DATA_SUBJECT_RIGHTS_RECTIFICATION"
    DPA_DATA_SUBJECT_RIGHTS_ERASURE = "DPA_DATA_SUBJECT_RIGHTS_ERASURE"
    DPA_DATA_SECURITY = "DPA_DATA_SECURITY"
    DPA_DATA_BREACH_NOTIFICATION = "DPA_DATA_BREACH_NOTIFICATION"
    DPA_DATA_RETENTION = "DPA_DATA_RETENTION"

    # Tenancy Laws (Landlord and Tenant Act, Rent Restriction Act, Distress for Rent Act)
    TENANCY_LEASE_MANDATORY_CLAUSES = "TENANCY_LEASE_MANDATORY_CLAUSES"
    TENANCY_RENT_INCREMENT_RULES = "TENANCY_RENT_INCREMENT_RULES"
    TENANCY_TERMINATION_NOTICE_PERIODS = "TENANCY_TERMINATION_NOTICE_PERIODS"
    TENANCY_SECURITY_DEPOSIT_RULES = "TENANCY_SECURITY_DEPOSIT_RULES" # Max amount, deductions, refund timeline
    TENANCY_REPAIR_OBLIGATIONS = "TENANCY_REPAIR_OBLIGATIONS"
    TENANCY_RENT_RECEIPT_REQUIREMENTS = "TENANCY_RENT_RECEIPT_REQUIREMENTS"
    TENANCY_LATE_FEE_POLICY = "TENANCY_LATE_FEE_POLICY"
    TENANCY_DISTRESS_FOR_RENT_PROCEDURE = "TENANCY_DISTRESS_FOR_RENT_PROCEDURE"
    TENANCY_EVICTION_PROCEDURES = "TENANCY_EVICTION_PROCEDURES"

    # Other
    CONSUMER_PROTECTION_FAIR_PRACTICES = "CONSUMER_PROTECTION_FAIR_PRACTICES"
    COMPETITION_MARKET_PRACTICES = "COMPETITION_MARKET_PRACTICES"
    ACCESSIBILITY_STANDARDS = "ACCESSIBILITY_STANDARDS" # If applicable
    MPESA_PAYMENT_REGULATIONS = "MPESA_PAYMENT_REGULATIONS" # e.g. CBK guidelines

    SYSTEM_OTHER = "SYSTEM_OTHER"

class ComplianceStatus(Enum): # From initial P5 outline, seems robust enough
    IDENTIFIED = "IDENTIFIED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ACTION_REQUIRED = "ACTION_REQUIRED"
    IMPLEMENTATION_IN_PROGRESS = "IMPLEMENTATION_IN_PROGRESS"
    IMPLEMENTED = "IMPLEMENTED"
    MONITORING = "MONITORING"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class ComplianceNote:
    def __init__(self,
                 note_id: int,
                 area_of_system: ComplianceArea,
                 kenyan_regulation_reference: str, # e.g., "Data Protection Act, 2019"
                 system_implication_notes: str, # Moved here, as it's required
                 specific_section_clause: Optional[str] = None, # e.g., "Section 26", "Clause 5.1.b"
                 system_components_affected: Optional[List[str]] = None, # e.g., ["UserAPI", "LeaseAdminUI", "NotificationService"]
                 action_taken_summary: Optional[str] = None,
                 status: ComplianceStatus = ComplianceStatus.IDENTIFIED,
                 assigned_to_user_id: Optional[int] = None, # FK to User (internal team member)
                 last_reviewed_at: datetime = datetime.utcnow(),
                 next_review_date: Optional[date] = None,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.note_id = note_id
        self.area_of_system = area_of_system
        self.kenyan_regulation_reference = kenyan_regulation_reference
        self.specific_section_clause = specific_section_clause
        self.system_components_affected = system_components_affected if system_components_affected is not None else []
        self.system_implication_notes = system_implication_notes
        self.action_taken_summary = action_taken_summary
        self.status = status
        self.assigned_to_user_id = assigned_to_user_id
        self.last_reviewed_at = last_reviewed_at
        self.next_review_date = next_review_date
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# dpa_consent_note = ComplianceNote(
#     note_id=1,
#     area_of_system=ComplianceArea.DPA_CONSENT_MANAGEMENT,
#     kenyan_regulation_reference="Data Protection Act, 2019",
#     specific_section_clause="Section 30 - Consent",
#     system_components_affected=["User Registration API", "User Profile UI", "Rental Application Form"],
#     system_implication_notes="System must obtain explicit, granular consent for data processing activities. " \
#                              "User.data_processing_consent_details field to store these. " \
#                              "Must be easy for users to withdraw consent.",
#     status=ComplianceStatus.ACTION_REQUIRED,
#     assigned_to_user_id=5 # Internal compliance officer
# )
# print(dpa_consent_note.area_of_system, dpa_consent_note.specific_section_clause)
