from datetime import datetime
from typing import Optional

class Message:
    def __init__(self,
                 message_id: int,
                 sender_id: int,    # Foreign Key to User
                 receiver_id: int,  # Foreign Key to User
                 content: str,
                 lease_id: Optional[int] = None, # FK to Lease, provides context (property, specific tenancy)
                 conversation_id: Optional[str] = None, # Can be derived: e.g., sorted(sender_id, receiver_id) + lease_id
                 has_attachments: bool = False, # True if there are associated attachments (actual attachment model is future)
                 sent_at: datetime = datetime.utcnow(),
                 read_at: Optional[datetime] = None,
                 updated_at: datetime = datetime.utcnow()): # If messages can be edited (less common) or to track read status changes

        self.message_id = message_id
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.content = content
        self.lease_id = lease_id # If the message is regarding a specific lease

        # If conversation_id is not provided, it could be generated.
        # Example: f"{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}_{lease_id or 'direct'}"
        self.conversation_id = conversation_id

        self.has_attachments = has_attachments # Simple flag for MVP
        self.sent_at = sent_at
        self.read_at = read_at # Timestamp when the receiver marked the message/conversation as read
        self.updated_at = updated_at


# Example usage:
# msg_lease_context = Message(
#     message_id=1, sender_id=10, receiver_id=20, # Landlord to Tenant
#     content="Regarding your maintenance request for unit 5A (Lease #101)...",
#     lease_id=101
# )
# if msg_lease_context.conversation_id is None:
#     ids = sorted([msg_lease_context.sender_id, msg_lease_context.receiver_id])
#     conv_suffix = f"lease_{msg_lease_context.lease_id}" if msg_lease_context.lease_id else "direct"
#     msg_lease_context.conversation_id = f"{ids[0]}_{ids[1]}_{conv_suffix}"
#
# print(msg_lease_context.content, msg_lease_context.conversation_id)
#
# msg_general = Message(
#     message_id=2, sender_id=20, receiver_id=10, # Tenant to Landlord
#     content="I have a general question about community rules."
#     # lease_id is None here
# )
# print(msg_general.content)
