from datetime import datetime
from typing import Optional
from hermitta_app import db
from .enums import NotificationType, NotificationChannel, NotificationStatus # Import from shared enums

class Notification(db.Model):
    __tablename__ = 'notifications'

    notification_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True) # Recipient User ID

    notification_type = db.Column(db.Enum(NotificationType), nullable=False, index=True)
    channel = db.Column(db.Enum(NotificationChannel), nullable=False, index=True) # e.g., EMAIL, SMS, IN_APP

    # Content can be pre-generated or generated at send time using a template
    subject = db.Column(db.Text, nullable=True) # For email notifications mainly
    content = db.Column(db.Text, nullable=True)

    template_id = db.Column(db.Integer, db.ForeignKey('notification_templates.template_id'), nullable=True, index=True)
    # JSON data for filling template placeholders if content/subject are not pre-generated
    template_context = db.Column(db.JSON, nullable=True)

    status = db.Column(db.Enum(NotificationStatus), default=NotificationStatus.PENDING, nullable=False, index=True)

    scheduled_send_time = db.Column(db.DateTime, nullable=True, index=True) # For prescheduled notifications
    sent_at = db.Column(db.DateTime, nullable=True) # Actual time it was dispatched
    delivered_at = db.Column(db.DateTime, nullable=True) # Actual time delivery was confirmed by gateway (if applicable)
    read_at = db.Column(db.DateTime, nullable=True, index=True) # For IN_APP notifications primarily

    # Contextual links
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=True, index=True)
    # reminder_rule_id = db.Column(db.Integer, db.ForeignKey('landlord_reminder_rules.rule_id'), nullable=True, index=True) # If we create LandlordReminderRule model
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), nullable=True, index=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.message_id'), nullable=True, index=True)
    maintenance_request_id = db.Column(db.Integer, db.ForeignKey('maintenance_requests.request_id'), nullable=True, index=True)
    document_id = db.Column(db.Integer, db.ForeignKey('documents.document_id'), nullable=True, index=True)

    # More generic way to link to any related entity if the above are not sufficient
    related_entity_type = db.Column(db.String(100), nullable=True) # e.g., 'PROPERTY', 'RENTAL_APPLICATION'
    related_entity_id = db.Column(db.Integer, nullable=True)   # ID of the related entity

    # Store error message from gateway if sending failed
    error_message = db.Column(db.Text, nullable=True)
    # Store external ID from notification provider (e.g., SendGrid message ID, Twilio SID)
    external_id = db.Column(db.String(255), nullable=True, index=True)


    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))
    template = db.relationship('NotificationTemplate', backref=db.backref('notifications_sent', lazy='dynamic'))
    lease = db.relationship('Lease', backref=db.backref('notifications', lazy='dynamic'))
    payment = db.relationship('Payment', backref=db.backref('notifications', lazy='dynamic'))
    message = db.relationship('Message', backref=db.backref('notifications', lazy='dynamic')) # e.g. a "new message" notification
    maintenance_request = db.relationship('MaintenanceRequest', backref=db.backref('notifications', lazy='dynamic'))
    document = db.relationship('Document', backref=db.backref('notifications', lazy='dynamic'))
    # reminder_rule = db.relationship('LandlordReminderRule', backref='triggered_notifications') # Future

    def __repr__(self):
        return f"<Notification {self.notification_id} for User {self.user_id} - Type: {self.notification_type.value} Channel: {self.channel.value} Status: {self.status.value}>"

    def mark_as_read(self):
        if not self.read_at:
            self.read_at = datetime.utcnow()
            self.status = NotificationStatus.READ
            # db.session.add(self) # Caller handles commit

    def mark_as_sent(self, external_id: Optional[str] = None, error: Optional[str] = None):
        self.sent_at = datetime.utcnow()
        if error:
            self.status = NotificationStatus.FAILED
            self.error_message = error
        else:
            self.status = NotificationStatus.SENT
            self.error_message = None # Clear previous errors
        if external_id:
            self.external_id = external_id
        # db.session.add(self) # Caller handles commit

    def mark_as_delivered(self, error: Optional[str] = None):
        self.delivered_at = datetime.utcnow()
        if error:
            self.status = NotificationStatus.DELIVERY_FAILURE
            self.error_message = error
        else:
            self.status = NotificationStatus.DELIVERED
            self.error_message = None
        # db.session.add(self) # Caller handles commit
