from enum import Enum
from datetime import datetime
from typing import Optional

class ComplianceArea(Enum):
    # General
    DATA_PROTECTION_PRIVACY = "DATA_PROTECTION_PRIVACY" # Kenya Data Protection Act, 2019

    # Lease Related
    LEASE_AGREEMENT_CLAUSES = "LEASE_AGREEMENT_CLAUSES"
    RENT_INCREMENTS = "RENT_INCREMENTS"
    TERMINATION_NOTICE_PERIODS = "TERMINATION_NOTICE_PERIODS"
    SECURITY_DEPOSIT_HANDLING = "SECURITY_DEPOSIT_HANDLING" # Limits, deductions, return
    REPAIR_OBLIGATIONS = "REPAIR_OBLIGATIONS" # Landlord vs Tenant responsibilities

    # Rent Collection
    RENT_RECEIPTS = "RENT_RECEIPTS" # Official receipt requirements
    LATE_FEE_POLICY = "LATE_FEE_POLICY" # Legality and limits
    RENT_ARREARS_PROCEDURES = "RENT_ARREARS_PROCEDURES" # e.g., Distress for Rent Act

    # Eviction
    EVICTION_COMMUNICATIONS = "EVICTION_COMMUNICATIONS" # Alignment with legal process

    # Tenant Screening
    SCREENING_CONSENT_PRIVACY = "SCREENING_CONSENT_PRIVACY"

    # Maintenance
    MAINTENANCE_RESPONSE_TIMELINESS = "MAINTENANCE_RESPONSE_TIMELINESS"

    # Dispute Resolution
    DISPUTE_RESOLUTION_INFO = "DISPUTE_RESOLUTION_INFO" # Providing info on official channels

    OTHER = "OTHER"

class ComplianceStatus(Enum):
    IDENTIFIED = "IDENTIFIED"               # Regulation/area identified as relevant
    UNDER_REVIEW = "UNDER_REVIEW"           # Actively being reviewed for system impact
    ACTION_REQUIRED = "ACTION_REQUIRED"     # Specific changes/features needed in the system
    IMPLEMENTATION_IN_PROGRESS = "IMPLEMENTATION_IN_PROGRESS" # Dev work ongoing
    IMPLEMENTED = "IMPLEMENTED"             # Changes made and verified
    MONITORING = "MONITORING"               # Implemented, but needs ongoing monitoring for changes/effectiveness
    NOT_APPLICABLE = "NOT_APPLICABLE"       # Reviewed and deemed not applicable

class ComplianceNote:
    def __init__(self,
                 note_id: int,
                 area_of_system: ComplianceArea, # Or string if more flexibility needed initially
                 kenyan_regulation_reference: Optional[str] = None, # e.g., "Landlord and Tenant Act, Section X"
                 system_implication_notes: Optional[str] = None, # How it affects system design/functionality
                 status: ComplianceStatus = ComplianceStatus.IDENTIFIED,
                 assigned_to_user_id: Optional[int] = None, # FK to User (internal team member)
                 last_reviewed_at: datetime = datetime.utcnow(),
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.note_id = note_id
        self.area_of_system = area_of_system # Could be ComplianceArea(area_of_system).value
        self.kenyan_regulation_reference = kenyan_regulation_reference
        self.system_implication_notes = system_implication_notes
        self.status = status
        self.assigned_to_user_id = assigned_to_user_id
        self.last_reviewed_at = last_reviewed_at
        self.created_at = created_at
        self.updated_at = updated_at

# Example usage:
# note1 = ComplianceNote(
#     note_id=1,
#     area_of_system=ComplianceArea.SECURITY_DEPOSIT_HANDLING,
#     kenyan_regulation_reference="The Landlord and Tenant Act (Cap. 301), Section on Deposits",
#     system_implication_notes="System must allow configuration of max security deposit (e.g., 2x rent). "
#                              "Track reasons for deductions. Ensure refund timelines can be managed.",
#     status=ComplianceStatus.ACTION_REQUIRED,
#     assigned_to_user_id=5 # Internal compliance officer
# )
# print(note1.area_of_system, note1.status)
