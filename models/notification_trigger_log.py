from datetime import datetime
from hermitta_app import db

class NotificationTriggerLog(db.Model):
    __tablename__ = 'notification_trigger_logs'

    log_id = db.Column(db.Integer, primary_key=True)

    # Foreign key to the rule that triggered this notification
    rule_id = db.Column(db.Integer, db.ForeignKey('landlord_reminder_rules.rule_id'), nullable=False, index=True)

    # Foreign key to the lease this notification pertains to (for lease-related rules)
    lease_id = db.Column(db.Integer, db.ForeignKey('leases.lease_id'), nullable=False, index=True)
    # Could be generalized with target_entity_type/id if rules apply to more than leases

    # The specific date of the event instance this log entry is for
    # (e.g., if a lease has end_date 2024-12-31, this would be 2024-12-31)
    target_event_date = db.Column(db.Date, nullable=False, index=True)

    # Foreign key to the actual notification that was created
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.notification_id'), nullable=False, unique=True, index=True)

    # Optional: An identifier for the specific job execution that created this log entry
    job_run_id = db.Column(db.String(255), nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    rule = db.relationship('LandlordReminderRule', backref=db.backref('trigger_logs', lazy='dynamic'))
    lease = db.relationship('Lease', backref=db.backref('reminder_trigger_logs', lazy='dynamic'))
    notification = db.relationship('Notification', backref=db.backref('trigger_log', uselist=False, lazy='joined')) # One-to-one

    # Unique constraint to prevent processing the same rule for the same lease and same event date multiple times
    __table_args__ = (db.UniqueConstraint('rule_id', 'lease_id', 'target_event_date', name='_rule_lease_event_uc'),)

    def __repr__(self):
        return f"<NotificationTriggerLog {self.log_id} - Rule: {self.rule_id}, Lease: {self.lease_id}, EventDate: {self.target_event_date}, Notification: {self.notification_id}>"
