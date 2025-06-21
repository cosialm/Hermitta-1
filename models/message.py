from datetime import datetime
from typing import Optional
from hermitta_app import db
from .enums import MessageType, MessageStatus

class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)

    sender_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True) # For direct messages

    # For messages related to a specific lease or property context
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=True, index=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.property_id'), nullable=True, index=True)
    # Note: If lease_id is present, property_id can often be derived.
    # Including property_id allows messages about a property not tied to a specific lease (e.g. to all tenants of a property).

    # To group messages into conversations.
    # Could be generated e.g., f"user_{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}" for direct chats
    # or f"lease_{lease_id}" for lease-specific chats.
    # Or a UUID if conversations can involve more than two people or have more complex grouping.
    conversation_id = db.Column(db.String(255), nullable=True, index=True)

    subject = db.Column(db.String(255), nullable=True) # Optional subject line
    content = db.Column(db.Text, nullable=False)

    message_type = db.Column(db.Enum(MessageType), default=MessageType.DIRECT_MESSAGE, nullable=False)
    status = db.Column(db.Enum(MessageStatus), default=MessageStatus.SENT, nullable=False, index=True)

    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True) # Timestamp when the primary receiver read the message

    # For future use with an Attachment model
    has_attachments = db.Column(db.Boolean, default=False, nullable=False)
    # Example: attachment_count = db.Column(db.Integer, default=0)
    # Example: attachments = db.relationship('MessageAttachment', backref='message', lazy='dynamic')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy='dynamic'))
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref=db.backref('received_messages', lazy='dynamic'))
    lease = db.relationship('Lease', backref=db.backref('messages', lazy='dynamic'))
    property = db.relationship('Property', backref=db.backref('messages', lazy='dynamic'))

    def __repr__(self):
        return f"<Message {self.message_id} from User {self.sender_id} to User {self.receiver_id} - Type: {self.message_type.value}>"

    # Helper method to mark as read
    def mark_as_read(self):
        if not self.read_at:
            self.read_at = datetime.utcnow()
            self.status = MessageStatus.READ
            # db.session.add(self) # Caller should handle session commit

    # Potential methods for conversation ID generation if not set externally:
    # def ensure_conversation_id(self):
    #     if not self.conversation_id:
    #         if self.message_type == MessageType.DIRECT_MESSAGE and self.sender_id and self.receiver_id:
    #             ids = sorted([self.sender_id, self.receiver_id])
    #             self.conversation_id = f"user_{ids[0]}_{ids[1]}"
    #         elif self.message_type == MessageType.LEASE_MESSAGE and self.lease_id:
    #             self.conversation_id = f"lease_{self.lease_id}"
    #         # Add other generation logic as needed
    #         # This might be better handled in a service layer before saving.
