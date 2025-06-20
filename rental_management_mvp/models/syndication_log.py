from enum import Enum
from datetime import datetime
from typing import Optional

class SyndicationStatus(Enum):
    PENDING = "PENDING"     # Queued for syndication
    IN_PROGRESS = "IN_PROGRESS" # Syndication attempt underway
    SUCCESS = "SUCCESS"     # Successfully listed/updated on the target platform
    FAILED = "FAILED"       # Failed to syndicate
    REMOVED = "REMOVED"     # Listing was successfully removed from the platform
    REMOVAL_FAILED = "REMOVAL_FAILED" # Failed to remove listing

class SyndicationLog:
    def __init__(self,
                 log_id: int,
                 property_id: int, # Foreign Key to Property
                 target_platform_name: str, # e.g., "JumiaHouse", "Property24Kenya", "GenericXMLFeed"
                 status: SyndicationStatus,
                 action: str, # e.g., "LIST", "UPDATE", "DELIST"
                 last_attempted_at: datetime = datetime.utcnow(),
                 details: Optional[str] = None, # Error messages, success confirmation, platform-specific listing ID
                 request_payload: Optional[str] = None, # What was sent to the platform (for debugging)
                 response_payload: Optional[str] = None # What was received from the platform (for debugging)
                 ):

        self.log_id = log_id
        self.property_id = property_id
        self.target_platform_name = target_platform_name
        self.status = status
        self.action = action # What action was being attempted
        self.last_attempted_at = last_attempted_at
        self.details = details # Can store platform's listing ID on success, or error message on failure
        self.request_payload = request_payload # Potentially large, consider storage implications
        self.response_payload = response_payload # Potentially large

# Example usage:
# log_entry_success = SyndicationLog(
#     log_id=1, property_id=101, target_platform_name="Property24Kenya",
#     status=SyndicationStatus.SUCCESS, action="LIST",
#     details="Successfully listed with ID P24-98765"
# )
#
# log_entry_failure = SyndicationLog(
#     log_id=2, property_id=102, target_platform_name="JumiaHouse",
#     status=SyndicationStatus.FAILED, action="UPDATE",
#     last_attempted_at=datetime.utcnow(),
#     details="Error: Missing required field 'neighborhood'.",
#     request_payload="{...}"
# )
# print(log_entry_success.target_platform_name, log_entry_success.status)
# print(log_entry_failure.target_platform_name, log_entry_failure.details)
