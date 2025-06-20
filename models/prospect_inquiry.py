from enum import Enum
from datetime import datetime
from typing import Optional

class ProspectInquiryStatus(Enum):
    NEW = "NEW"                     # Inquiry just received
    CONTACTED = "CONTACTED"           # Landlord/agent has responded or attempted contact
    VIEWING_SCHEDULED = "VIEWING_SCHEDULED" # A property viewing has been scheduled
    APPLICATION_INVITED = "APPLICATION_INVITED" # Prospect invited to fill out rental application
    ARCHIVED_NO_INTEREST = "ARCHIVED_NO_INTEREST" # Prospect no longer interested or unresponsive
    ARCHIVED_PROPERTY_UNAVAILABLE = "ARCHIVED_PROPERTY_UNAVAILABLE" # Property leased to someone else
    OTHER = "OTHER"

class ProspectInquiry:
    def __init__(self,
                 inquiry_id: int,
                 property_id: int, # Foreign Key to Property the inquiry is about
                 landlord_id: int, # Foreign Key to User (Landlord who owns the property)
                 prospect_name: str,
                 prospect_email: str, # Consider validation
                 prospect_phone: Optional[str] = None, # Consider validation
                 message: Optional[str] = None, # Prospect's message
                 preferred_contact_method: Optional[str] = None, # e.g., "EMAIL", "PHONE"
                 source: Optional[str] = None, # e.g., "Website Form", "JumiaHouse", "Property24"
                 received_at: datetime = datetime.utcnow(),
                 status: ProspectInquiryStatus = ProspectInquiryStatus.NEW,
                 internal_notes: Optional[str] = None, # Landlord's notes about this prospect/inquiry
                 updated_at: datetime = datetime.utcnow()):

        self.inquiry_id = inquiry_id
        self.property_id = property_id
        self.landlord_id = landlord_id # To associate inquiry with the property owner

        self.prospect_name = prospect_name
        self.prospect_email = prospect_email
        self.prospect_phone = prospect_phone
        self.message = message

        self.preferred_contact_method = preferred_contact_method
        self.source = source # Helps track where inquiries are coming from

        self.received_at = received_at
        self.status = status
        self.internal_notes = internal_notes # For landlord to manage interactions
        self.updated_at = updated_at

# Example Usage:
# inquiry1 = ProspectInquiry(
#     inquiry_id=1, property_id=101, landlord_id=10,
#     prospect_name="Jane Doe",
#     prospect_email="jane.doe@example.com",
#     prospect_phone="+254712345678",
#     message="I am very interested in the 2-bedroom apartment on Main St. When can I schedule a viewing?",
#     preferred_contact_method="PHONE",
#     source="Website Listing"
# )
#
# # After landlord contacts Jane:
# # inquiry1.status = ProspectInquiryStatus.CONTACTED
# # inquiry1.internal_notes = "Called Jane on 2024-03-15, scheduled viewing for 2024-03-17 2PM."
# # inquiry1.updated_at = datetime.utcnow()
#
# print(inquiry1.prospect_name, inquiry1.property_id, inquiry1.status)
