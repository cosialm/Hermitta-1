from enum import Enum
from datetime import datetime
from typing import Optional

class ReminderOffsetRelativeTo(Enum):
    RENT_DUE_DATE = "RENT_DUE_DATE"
    LEASE_START_DATE = "LEASE_START_DATE"
    LEASE_END_DATE = "LEASE_END_DATE" # For lease renewal reminders

class LandlordReminderRule:
    def __init__(self,
                 rule_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord)
                 template_id: int, # Foreign Key to NotificationTemplate
                 name: str, # Landlord's name for this rule, e.g., "7-Day Rent Reminder for All Properties"
                 days_offset: int, # e.g., -7 for 7 days before, 3 for 3 days after. 0 for on the day.
                 offset_relative_to: ReminderOffsetRelativeTo,
                 # Optional: Apply rule only to specific properties or property types
                 # property_ids: Optional[List[int]] = None, # Apply to specific properties
                 # property_types: Optional[List[PropertyType]] = None, # Apply to specific property types
                 send_time_hour: int = 9, # Hour of the day to send (0-23) in landlord's timezone (or system default)
                 send_time_minute: int = 0,
                 is_active: bool = True,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.rule_id = rule_id
        self.landlord_id = landlord_id
        self.template_id = template_id # The NotificationTemplate to use
        self.name = name

        self.days_offset = days_offset
        self.offset_relative_to = offset_relative_to

        self.send_time_hour = send_time_hour   # e.g., 9 for 9 AM
        self.send_time_minute = send_time_minute # e.g., 0 for on the hour

        self.is_active = is_active # Only active rules are processed by the scheduler

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# rule1 = LandlordReminderRule(
#     rule_id=1, landlord_id=10, template_id=1, # Assuming template_id 1 is "SMS Rent Reminder - 7 Days"
#     name="Standard 7-Day SMS Rent Reminder",
#     days_offset=-7, # 7 days BEFORE rent_due_date
#     offset_relative_to=ReminderOffsetRelativeTo.RENT_DUE_DATE,
#     send_time_hour=10, # 10:00 AM
#     is_active=True
# )
#
# rule2 = LandlordReminderRule(
#     rule_id=2, landlord_id=10, template_id=5, # Assuming template_id 5 is "Lease Renewal Reminder - 60 Days"
#     name="Lease Renewal Reminder - 60 Days Before End",
#     days_offset=-60, # 60 days BEFORE lease_end_date
#     offset_relative_to=ReminderOffsetRelativeTo.LEASE_END_DATE,
#     send_time_hour=11
# )
# print(rule1.name, rule1.days_offset, rule1.offset_relative_to)
