from datetime import datetime, time
from typing import Optional
from hermitta_app import db
from .enums import ReminderRuleEvent, ReminderRecipientType, ReminderTimeUnit

class LandlordReminderRule(db.Model):
    __tablename__ = 'landlord_reminder_rules'

    rule_id = db.Column(db.Integer, primary_key=True)
    landlord_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False) # Landlord's name for this rule

    # Triggering event
    event_type = db.Column(db.Enum(ReminderRuleEvent), nullable=False, index=True)

    # Offset from the event
    offset_value = db.Column(db.Integer, nullable=False) # e.g., 7, -3, 2
    offset_unit = db.Column(db.Enum(ReminderTimeUnit), nullable=False) # e.g., DAYS, WEEKS
                                                                    # Negative offset_value means "before", positive means "after"
                                                                    # Example: offset_value=-7, offset_unit=DAYS means 7 days before event_type

    # Time of day to send the reminder
    send_time = db.Column(db.Time, default=time(9,0), nullable=False) # Defaults to 09:00 AM

    # Who receives this reminder
    recipient_type = db.Column(db.Enum(ReminderRecipientType), default=ReminderRecipientType.TENANT, nullable=False)
    # If recipient_type is OTHER_USER, this specifies the user_id
    specific_recipient_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True, index=True)
    # If recipient_type is CUSTOM_EMAIL, this stores the email address
    custom_recipient_email = db.Column(db.String(255), nullable=True)

    # Which notification template to use for this reminder
    notification_template_id = db.Column(db.Integer, db.ForeignKey('notification_templates.template_id'), nullable=False, index=True)

    # Scope: Apply to all properties of the landlord, or specific ones?
    # For MVP, could be all. Future: link to properties or property groups.
    # property_scope_type (Enum: ALL, SPECIFIC_PROPERTIES, PROPERTY_GROUP)
    # property_ids (JSON list of property_id if SPECIFIC_PROPERTIES)
    # property_group_id (FK if PROPERTY_GROUP)

    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    landlord = db.relationship('User', foreign_keys=[landlord_id], backref=db.backref('reminder_rules', lazy='dynamic'))
    notification_template = db.relationship('NotificationTemplate', backref=db.backref('linked_reminder_rules', lazy='dynamic'))
    specific_recipient_user = db.relationship('User', foreign_keys=[specific_recipient_user_id], backref=db.backref('custom_reminder_rules_recipient', lazy='dynamic'))

    def __repr__(self):
        return f"<LandlordReminderRule {self.rule_id} '{self.name}' for Landlord {self.landlord_id} Event: {self.event_type.value}>"

    # Logic to calculate next send datetime would typically be in a service layer,
    # querying these rules and relevant event dates (e.g., lease end dates, rent due dates).
    # Example:
    # def get_next_trigger_datetime_for_lease(self, lease):
    #     event_date = None
    #     if self.event_type == ReminderRuleEvent.RENT_DUE_DATE:
    #         # Complex: need to know current/next rent due date for the lease
    #         pass
    #     elif self.event_type == ReminderRuleEvent.LEASE_END_DATE:
    #         event_date = lease.end_date
    #     # ... other event types ...
    #
    #     if event_date:
    #         # Calculate offset (this needs timedelta logic based on offset_unit)
    #         # For now, simplified for DAYS:
    #         if self.offset_unit == ReminderTimeUnit.DAYS:
    #             trigger_date = event_date + timedelta(days=self.offset_value)
    #             return datetime.combine(trigger_date, self.send_time)
    #     return None
