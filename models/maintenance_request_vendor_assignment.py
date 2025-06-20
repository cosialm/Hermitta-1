from enum import Enum
from datetime import datetime
from typing import Optional

# Assuming MaintenanceRequest model exists in models.maintenance_request
# Assuming User model (for Vendor) exists in models.user
# Assuming Quote model exists in models.quote

class VendorAssignmentStatus(Enum):
    PENDING_ACCEPTANCE = "PENDING_ACCEPTANCE" # Vendor has been assigned, awaiting their acceptance
    ACCEPTED = "ACCEPTED"                  # Vendor has accepted the assignment
    DECLINED = "DECLINED"                  # Vendor has declined the assignment
    WORK_IN_PROGRESS = "WORK_IN_PROGRESS"    # Vendor has started work (if applicable after quote approval)
    COMPLETED_BY_VENDOR = "COMPLETED_BY_VENDOR" # Vendor marked their part as complete
    CANCELLED_BY_LANDLORD = "CANCELLED_BY_LANDLORD" # Landlord cancelled assignment for this vendor

class MaintenanceRequestVendorAssignment:
    def __init__(self,
                 assignment_id: int, # PK
                 request_id: int,    # FK to MaintenanceRequest
                 vendor_id: int,     # FK to User (where User.role == VENDOR)
                 assigned_at: datetime = datetime.utcnow(),
                 status: VendorAssignmentStatus = VendorAssignmentStatus.PENDING_ACCEPTANCE,
                 # Link to the vendor's quote for this specific request, if they submit one.
                 # This implies a Quote would also have a vendor_id and request_id.
                 vendor_quote_id: Optional[int] = None, # FK to Quote model
                 # Optional: Specific instructions or scope for this vendor on this request
                 vendor_specific_instructions: Optional[str] = None,
                 # Timestamps for status changes
                 accepted_at: Optional[datetime] = None,
                 declined_at: Optional[datetime] = None,
                 work_started_at: Optional[datetime] = None,
                 work_completed_at: Optional[datetime] = None,
                 cancelled_at: Optional[datetime] = None):

        self.assignment_id = assignment_id
        self.request_id = request_id
        self.vendor_id = vendor_id
        self.assigned_at = assigned_at
        self.status = status
        self.vendor_quote_id = vendor_quote_id
        self.vendor_specific_instructions = vendor_specific_instructions

        self.accepted_at = accepted_at
        self.declined_at = declined_at
        self.work_started_at = work_started_at
        self.work_completed_at = work_completed_at
        self.cancelled_at = cancelled_at

# Example Usage:
# assignment1 = MaintenanceRequestVendorAssignment(
#     assignment_id=1,
#     request_id=101, # MaintenanceRequest ID
#     vendor_id=51,   # User ID of a Vendor
#     status=VendorAssignmentStatus.PENDING_ACCEPTANCE
# )
#
# # When vendor accepts:
# # assignment1.status = VendorAssignmentStatus.ACCEPTED
# # assignment1.accepted_at = datetime.utcnow()
#
# # If vendor submits a quote (Quote ID 789):
# # assignment1.vendor_quote_id = 789
#
# print(f"Assignment {assignment1.assignment_id} for Request {assignment1.request_id} to Vendor {assignment1.vendor_id} is {assignment1.status}")
