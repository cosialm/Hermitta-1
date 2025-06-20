from datetime import datetime
from typing import Optional

class MaintenanceCommunication:
    def __init__(self,
                 comm_id: int,
                 maintenance_request_id: int, # Foreign Key to MaintenanceRequest
                 user_id: int, # Foreign Key to User (Tenant, Landlord, Staff, or Vendor sending message)
                 message_text: str,
                 # For MVP, attachments on comms might be complex.
                 # Could link to MaintenanceAttachment if needed, or just keep comms text-only.
                 # has_attachments: bool = False,
                 # attachment_ids: Optional[List[int]] = None, # List of MaintenanceAttachment IDs
                 sent_at: datetime = datetime.utcnow(),
                 is_internal_note: bool = False # True if this is a private note for landlord/staff, not visible to tenant/vendor
                 ):

        self.comm_id = comm_id
        self.maintenance_request_id = maintenance_request_id
        self.user_id = user_id # ID of the User who sent this message/note
        self.message_text = message_text
        self.sent_at = sent_at
        self.is_internal_note = is_internal_note # Differentiates between comms and private notes

# Example Usage:
# tenant_update = MaintenanceCommunication(
#     comm_id=1, maintenance_request_id=501, user_id=201, # Tenant
#     message_text="The plumber just left, and the leak seems to be fixed for now. I will monitor it."
# )
#
# landlord_note_to_staff = MaintenanceCommunication(
#     comm_id=2, maintenance_request_id=501, user_id=10, # Landlord
#     message_text="Staff_Member_X, please follow up with tenant tomorrow to confirm resolution.",
#     is_internal_note=True # This note is not visible to the tenant
# )
#
# vendor_comm = MaintenanceCommunication(
#     comm_id=3, maintenance_request_id=501, user_id=301, # Vendor
#     message_text="Scheduled the visit for tomorrow at 10 AM. Will need access to the main water shutoff."
# )
# print(tenant_update.message_text)
# print(landlord_note_to_staff.is_internal_note)
