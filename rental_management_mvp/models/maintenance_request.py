from enum import Enum
from datetime import datetime
from typing import Optional

# Refined for Phase 1 MVP (Basic)
class MaintenanceRequestStatus(Enum):
    SUBMITTED = "SUBMITTED"
    IN_PROGRESS = "IN_PROGRESS" # Landlord has acknowledged and is working on it
    RESOLVED = "RESOLVED"     # Landlord has marked it as work done
    CLOSED = "CLOSED"         # Tenant or Landlord confirms resolution and closes request

class MaintenanceRequestCategory(Enum):
    PLUMBING = "PLUMBING"
    ELECTRICAL = "ELECTRICAL"
    GENERAL_REPAIR = "GENERAL_REPAIR" # e.g., door, window, cupboard
    APPLIANCE = "APPLIANCE"       # e.g., cooker, fridge (if supplied by landlord)
    STRUCTURAL = "STRUCTURAL"     # e.g., cracks in wall, roof leak
    PEST_CONTROL = "PEST_CONTROL"
    OTHER = "OTHER"

class MaintenanceRequest:
    def __init__(self,
                 request_id: int,
                 property_id: int, # Foreign Key to Property
                 tenant_id: int,   # Foreign Key to User (Tenant)
                 description: str,
                 category: MaintenanceRequestCategory, # New field
                 status: MaintenanceRequestStatus = MaintenanceRequestStatus.SUBMITTED,
                 tenant_contact_preference: Optional[str] = None, # New field
                 submitted_at: datetime = datetime.utcnow(),
                 resolved_at: Optional[datetime] = None, # Timestamp when status changed to RESOLVED
                 updated_at: datetime = datetime.utcnow() # Timestamp of last update to the request
                 ):

        self.request_id = request_id
        self.property_id = property_id
        self.tenant_id = tenant_id
        self.description = description
        self.category = category
        self.status = status
        self.tenant_contact_preference = tenant_contact_preference # e.g., "Call me on 07XXXXXXXX"

        self.submitted_at = submitted_at
        self.resolved_at = resolved_at # Set when landlord marks as resolved
        self.updated_at = updated_at   # Updated on any change, including status changes

# Example Usage (Refined Phase 1):
# request1 = MaintenanceRequest(
#     request_id=1, property_id=101, tenant_id=201,
#     description="Kitchen tap is leaking constantly.",
#     category=MaintenanceRequestCategory.PLUMBING,
#     tenant_contact_preference="Please call John on +254712345678 before coming."
# )
#
# request2 = MaintenanceRequest(
#     request_id=2, property_id=102, tenant_id=202,
#     description="Main bedroom light not working.",
#     category=MaintenanceRequestCategory.ELECTRICAL,
#     status=MaintenanceRequestStatus.IN_PROGRESS
# )
# print(request1.category, request1.tenant_contact_preference)
# print(request2.category, request2.status)
