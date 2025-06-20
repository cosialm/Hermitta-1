from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any # For JSON payloads

class SyndicationAction(Enum):
    LIST = "LIST"     # Create new listing on platform
    UPDATE = "UPDATE"   # Update existing listing on platform
    DELIST = "DELIST"   # Remove listing from platform
    REFRESH = "REFRESH" # Refresh or extend existing listing

class SyndicationLogStatus(Enum): # From initial P6 outline, seems robust
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    REMOVED = "REMOVED"     # Confirmation of delisting
    REMOVAL_FAILED = "REMOVAL_FAILED"
    REQUIRES_MANUAL_ATTENTION = "REQUIRES_MANUAL_ATTENTION"

class SyndicationLog:
    def __init__(self,
                 log_id: int,
                 property_id: int, # Foreign Key to Property
                 platform_id: int, # Foreign Key to SyndicationPlatform
                 action: SyndicationAction, # What action was being attempted
                 status: SyndicationLogStatus = SyndicationLogStatus.PENDING,
                 landlord_syndication_setting_id: Optional[int] = None, # FK to LandlordSyndicationSetting used
                 last_attempted_at: Optional[datetime] = None, # Timestamp of the last attempt for this action
                 completed_at: Optional[datetime] = None, # Timestamp of success/failure/removal
                 details: Optional[str] = None, # Error messages, success confirmation, platform-specific listing ID
                 syndication_payload_sent: Optional[Dict[str, Any]] = None, # JSON of what was sent
                 platform_response: Optional[Dict[str, Any]] = None, # JSON of what was received
                 created_at: datetime = datetime.utcnow()):

        self.log_id = log_id
        self.property_id = property_id
        self.platform_id = platform_id # Links to SyndicationPlatform model
        self.action = action
        self.status = status
        self.landlord_syndication_setting_id = landlord_syndication_setting_id # Which landlord setting triggered this

        self.last_attempted_at = last_attempted_at if last_attempted_at else datetime.utcnow()
        self.completed_at = completed_at
        self.details = details

        self.syndication_payload_sent = syndication_payload_sent # For debugging/auditing
        self.platform_response = platform_response # For debugging/auditing

        self.created_at = created_at

# Example Usage:
# log_synd_list_p24 = SyndicationLog(
#     log_id=1, property_id=101, platform_id=1, # Platform 1 = Property24
#     action=SyndicationAction.LIST,
#     status=SyndicationLogStatus.IN_PROGRESS,
#     landlord_syndication_setting_id=5
# )
#
# # After successful attempt:
# # log_synd_list_p24.status = SyndicationLogStatus.SUCCESS
# # log_synd_list_p24.completed_at = datetime.utcnow()
# # log_synd_list_p24.details = "Successfully listed. Platform Listing ID: P24-XYZ123"
# # log_synd_list_p24.platform_response = {"id": "P24-XYZ123", "status": "active", ...}
#
# print(log_synd_list_p24.property_id, log_synd_list_p24.platform_id, log_synd_list_p24.action)
