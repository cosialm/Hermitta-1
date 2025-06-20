from enum import Enum
from datetime import datetime
from typing import Optional, List, Dict # For placeholders

# Re-using NotificationType from notification.py if it's generic enough,
# or define a specific TemplateType if needed. Assuming NotificationType exists.
# from .notification import NotificationType # If it's in another file in same dir
# For now, let's duplicate a simplified version for clarity if NotificationType isn't accessible
class NotificationTemplateType(Enum):
    RENT_REMINDER = "RENT_REMINDER"
    LATE_RENT_WARNING = "LATE_RENT_WARNING"
    PAYMENT_CONFIRMATION = "PAYMENT_CONFIRMATION" # For M-Pesa success
    PAYMENT_FAILED = "PAYMENT_FAILED"         # For M-Pesa failure
    NEW_MESSAGE_ALERT = "NEW_MESSAGE_ALERT"
    LEASE_UPDATE_ALERT = "LEASE_UPDATE_ALERT"
    # Add other template types as needed

class NotificationDeliveryMethod(Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    IN_APP = "IN_APP" # In-app notification within the platform

class NotificationTemplate:
    def __init__(self,
                 template_id: int,
                 name: str, # e.g., "Rent Reminder - 7 Days Before (SMS)", "Mpesa Payment Confirmation (Email)"
                 template_type: NotificationTemplateType,
                 delivery_method: NotificationDeliveryMethod,
                 subject_template_en: Optional[str] = None, # For emails, English
                 body_template_en: str, # English version with placeholders
                 subject_template_sw: Optional[str] = None, # For emails, Swahili
                 body_template_sw: Optional[str] = None, # Swahili version with placeholders
                 # Placeholders example: {{tenant_name}}, {{landlord_name}}, {{property_address}},
                 #                     {{rent_amount}}, {{due_date}}, {{payment_amount}}, {{receipt_number}}
                 required_placeholders: Optional[List[str]] = None, # List of expected placeholder names e.g. ["tenant_name", "rent_amount"]
                 is_system_template: bool = False, # True if it's a default system template, False if custom by landlord (future)
                 is_active: bool = True,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.template_id = template_id
        self.name = name
        self.template_type = template_type
        self.delivery_method = delivery_method

        self.subject_template_en = subject_template_en
        self.body_template_en = body_template_en
        self.subject_template_sw = subject_template_sw
        self.body_template_sw = body_template_sw if body_template_sw else body_template_en # Default to EN if SW not provided

        self.required_placeholders = required_placeholders if required_placeholders is not None else []
        self.is_system_template = is_system_template # System templates might not be editable by landlords
        self.is_active = is_active # Only active templates can be used

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# sms_rent_reminder_en = NotificationTemplate(
#     template_id=1, name="SMS Rent Reminder - 7 Days (EN)",
#     template_type=NotificationTemplateType.RENT_REMINDER,
#     delivery_method=NotificationDeliveryMethod.SMS,
#     body_template_en="Dear {{tenant_name}}, your rent of KES {{rent_amount}} for {{property_address}} is due on {{due_date}}. Thank you.",
#     body_template_sw="Mpendwa {{tenant_name}}, kodi yako ya KES {{rent_amount}} kwa {{property_address}} inastahili tarehe {{due_date}}. Asante.",
#     required_placeholders=["tenant_name", "rent_amount", "property_address", "due_date"],
#     is_system_template=True
# )
#
# email_payment_confirmation_en = NotificationTemplate(
#     template_id=2, name="Email M-Pesa Payment Confirmation (EN)",
#     template_type=NotificationTemplateType.PAYMENT_CONFIRMATION,
#     delivery_method=NotificationDeliveryMethod.EMAIL,
#     subject_template_en="Payment Confirmation for {{property_address}}",
#     body_template_en="Dear {{tenant_name}},\n\nWe have received your payment of KES {{payment_amount}} with receipt number {{receipt_number}} for {{property_address}}.\n\nThank you,\n{{landlord_name}}.",
#     required_placeholders=["tenant_name", "payment_amount", "receipt_number", "property_address", "landlord_name"],
#     is_system_template=True
# )
# print(sms_rent_reminder_en.name, sms_rent_reminder_en.delivery_method)
# print(email_payment_confirmation_en.subject_template_en)
