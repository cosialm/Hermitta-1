from datetime import datetime
from typing import Optional, List
from hermitta_app import db
from .enums import NotificationType, NotificationChannel # Import from shared enums

class NotificationTemplate(db.Model):
    __tablename__ = 'notification_templates'

    template_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True) # e.g., "Rent Reminder - 7 Days Before (SMS)"

    template_type = db.Column(db.Enum(NotificationType), nullable=False, index=True)
    channel = db.Column(db.Enum(NotificationChannel), nullable=False, index=True) # Renamed from delivery_method

    # For EMAIL channel
    subject_template_en = db.Column(db.Text, nullable=True)
    body_template_en = db.Column(db.Text, nullable=False) # English version with placeholders like {{variable_name}}

    # Optional Swahili versions
    subject_template_sw = db.Column(db.Text, nullable=True)
    body_template_sw = db.Column(db.Text, nullable=True)

    # List of expected placeholder names, e.g. ["tenant_name", "rent_amount"]. Stored as JSON.
    required_placeholders = db.Column(db.JSON, nullable=True)

    # True if it's a default system template (non-editable by landlords), False if custom by landlord (future feature)
    is_system_template = db.Column(db.Boolean, default=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False, index=True) # Only active templates can be used

    description = db.Column(db.Text, nullable=True) # Optional description of the template's purpose

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to Notifications (one template can be used by many notifications)
    # notifications = db.relationship('Notification', backref='template', lazy='dynamic') # Defined in Notification model

    def __repr__(self):
        return f"<NotificationTemplate {self.template_id} '{self.name}' Type: {self.template_type.value} Channel: {self.channel.value}>"

    def render_template(self, context: dict, language: str = 'en') -> dict:
        """
        Renders the template with the given context and language.
        Returns a dict with 'subject' and 'body'.
        Basic placeholder replacement, can be made more sophisticated.
        """
        subject = None
        body = None

        if language == 'sw':
            subject_tpl = self.subject_template_sw if self.subject_template_sw else self.subject_template_en
            body_tpl = self.body_template_sw if self.body_template_sw else self.body_template_en
        else: # Default to English
            subject_tpl = self.subject_template_en
            body_tpl = self.body_template_en

        if not body_tpl: # Should not happen if templates are well-defined
            raise ValueError(f"Body template for language '{language}' is missing for template ID {self.template_id}")

        if subject_tpl:
            subject = subject_tpl
            for key, value in context.items():
                subject = subject.replace(f"{{{{{key}}}}}", str(value))

        body = body_tpl
        for key, value in context.items():
            body = body.replace(f"{{{{{key}}}}}", str(value))

        return {"subject": subject, "body": body}
