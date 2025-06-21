import uuid
from datetime import datetime, date, timedelta, time
from typing import Optional # Added import for Optional
from flask import current_app
from hermitta_app import db
from models import (
    LandlordReminderRule, Lease, Notification, NotificationTemplate,
    NotificationTriggerLog, User, Property
)
# Corrected import for LeaseStatusType
from models.lease import LeaseStatusType
from models.enums import (
    ReminderRuleEvent, ReminderTimeUnit,
    NotificationStatus, NotificationChannel # MessageType is not used in this job currently
)

def process_lease_renewal_reminders_job(job_run_id: Optional[str] = None):
    """
    Processes active lease renewal reminder rules for landlords.

    This job queries for `LandlordReminderRule`s that are active and set for the
    `LEASE_END_DATE` event. For each rule, it calculates which leases should trigger
    a reminder today based on the rule's offset (e.g., 60 days before lease end).

    It checks against the `NotificationTriggerLog` to ensure that a reminder for a specific
    rule, lease, and lease end date combination has not already been processed.

    If a reminder is due, it fetches the associated `NotificationTemplate`, prepares
    the context with lease, property, tenant, and landlord details, and creates a new
    `Notification` record (typically with status 'SCHEDULED'). It also logs this action
    in the `NotificationTriggerLog`.

    The actual sending of notifications (email, SMS, etc.) is handled by a separate
    dispatcher system that would process 'SCHEDULED' notifications.

    This job is designed to be run periodically (e.g., daily via a cron job or
    other task scheduler) using the Flask CLI command:
    `flask run-lease-renewal-job`

    Args:
        job_run_id (Optional[str]): An optional unique identifier for this specific job run.
                                    If not provided, a UUID will be generated.
    """
    if job_run_id is None:
        job_run_id = str(uuid.uuid4())

    current_app.logger.info(f"Starting lease renewal reminder job (ID: {job_run_id}) for date: {date.today()}")

    active_rules = db.session.query(LandlordReminderRule).filter(
        LandlordReminderRule.is_active == True,
        LandlordReminderRule.event_type == ReminderRuleEvent.LEASE_END_DATE
    ).all()

    if not active_rules:
        current_app.logger.info("No active lease renewal reminder rules found.")
        return

    for rule in active_rules:
        current_app.logger.info(f"Processing rule ID: {rule.rule_id} ('{rule.name}') for landlord ID: {rule.landlord_id}")

        # Calculate the target lease end_date for which reminders should be sent today
        # Example: Rule is -60 DAYS. Today is D. Reminder is for leases ending on D + 60 DAYS.
        # So, lease.end_date = today + abs(offset_value) if offset is negative (before event)
        # Or, lease.end_date = today - offset_value if offset is positive (after event) - less common for renewals

        offset_days = 0
        if rule.offset_unit == ReminderTimeUnit.DAYS:
            offset_days = rule.offset_value
        elif rule.offset_unit == ReminderTimeUnit.WEEKS:
            offset_days = rule.offset_value * 7
        elif rule.offset_unit == ReminderTimeUnit.MONTHS:
            # This is an approximation; month lengths vary. For precise month offsets,
            # dateutil.relativedelta would be better. For simplicity, using 30 days.
            offset_days = rule.offset_value * 30
        else:
            current_app.logger.warning(f"Unsupported offset_unit {rule.offset_unit} for Rule ID {rule.rule_id}. Skipping.")
            continue

        # We want to find leases where (Lease.end_date + offset_days_as_timedelta) == today
        # This means Lease.end_date == today - offset_days_as_timedelta
        # If offset_days is -60 (60 days before), then target_lease_end_date = today - (-60 days) = today + 60 days
        target_lease_end_date = date.today() - timedelta(days=offset_days)

        current_app.logger.debug(f"Rule ID {rule.rule_id}: offset_days={offset_days}, target_lease_end_date={target_lease_end_date}")

        leases_to_remind = db.session.query(Lease).filter(
            Lease.landlord_id == rule.landlord_id,
            Lease.end_date == target_lease_end_date,
            Lease.status.in_([LeaseStatusType.ACTIVE, LeaseStatusType.ACTIVE_PENDING_MOVE_IN]) # Consider relevant active statuses
        ).all()

        if not leases_to_remind:
            current_app.logger.info(f"No leases found matching criteria for Rule ID {rule.rule_id} ending on {target_lease_end_date}.")
            continue

        current_app.logger.info(f"Found {len(leases_to_remind)} leases for Rule ID {rule.rule_id} ending on {target_lease_end_date}.")

        for lease in leases_to_remind:
            # Idempotency Check: Has this reminder been logged already?
            existing_log = db.session.query(NotificationTriggerLog).filter_by(
                rule_id=rule.rule_id,
                lease_id=lease.lease_id,
                target_event_date=lease.end_date # The actual end date of this lease
            ).first()

            if existing_log:
                current_app.logger.info(f"Reminder already processed for Rule ID {rule.rule_id}, Lease ID {lease.lease_id}, Event Date {lease.end_date}. Log ID: {existing_log.log_id}. Skipping.")
                continue

            template = db.session.query(NotificationTemplate).get(rule.notification_template_id)
            if not template:
                current_app.logger.error(f"NotificationTemplate ID {rule.notification_template_id} not found for Rule ID {rule.rule_id}. Skipping Lease ID {lease.lease_id}.")
                continue

            if not template.is_active:
                current_app.logger.warning(f"NotificationTemplate ID {template.template_id} ('{template.name}') is inactive. Skipping for Rule ID {rule.rule_id}, Lease ID {lease.lease_id}.")
                continue

            # Determine recipient
            recipient_user = None
            # For LEASE_END_DATE, typically the tenant is the primary recipient.
            # The rule.recipient_type can refine this.
            if rule.recipient_type == ReminderRecipientType.TENANT:
                recipient_user = lease.tenant_user
            elif rule.recipient_type == ReminderRecipientType.LANDLORD:
                recipient_user = rule.landlord
            elif rule.recipient_type == ReminderRecipientType.PROPERTY_MANAGER:
                # TODO: Implement logic if Property Manager role/assignment exists
                current_app.logger.warning(f"RecipientType PROPERTY_MANAGER not yet implemented for Rule ID {rule.rule_id}. Defaulting to landlord.")
                recipient_user = rule.landlord
            elif rule.recipient_type == ReminderRecipientType.OTHER_USER and rule.specific_recipient_user_id:
                recipient_user = db.session.query(User).get(rule.specific_recipient_user_id)
            else: # Fallback or unhandled recipient type for this event
                 current_app.logger.warning(f"Unhandled or invalid recipient_type '{rule.recipient_type}' for Rule ID {rule.rule_id}. Defaulting to tenant if available.")
                 recipient_user = lease.tenant_user

            if not recipient_user:
                current_app.logger.error(f"Could not determine recipient for Rule ID {rule.rule_id}, Lease ID {lease.lease_id}. Skipping.")
                continue

            # Prepare template context
            property_obj = lease.property
            context = {
                "tenant_name": lease.tenant_user.full_name if lease.tenant_user else (lease.tenant_name_manual or "Tenant"),
                "landlord_name": rule.landlord.full_name if rule.landlord else "Landlord/Property Manager",
                "lease_end_date": lease.end_date.strftime("%Y-%m-%d") if lease.end_date else "N/A",
                "days_offset": abs(offset_days), # Make it positive for display "X days remaining"
                "property_address": property_obj.address_line_1 if property_obj else "N/A",
                "property_unit": property_obj.unit_name or property_obj.unit_number if property_obj else "N/A",
                # Add other common placeholders
            }

            # Create Notification object
            scheduled_send_datetime = datetime.combine(date.today(), rule.send_time)

            new_notification = Notification(
                user_id=recipient_user.user_id,
                notification_type=template.template_type, # Use type from template
                channel=template.channel,
                template_id=template.template_id,
                template_context=context,
                status=NotificationStatus.SCHEDULED, # To be picked up by a dispatcher
                scheduled_send_time=scheduled_send_datetime,
                lease_id=lease.lease_id,
                # Potentially add more specific related_entity info if needed
                # related_entity_type="LEASE_RENEWAL_REMINDER",
                # related_entity_id=rule.rule_id
            )
            db.session.add(new_notification)
            db.session.flush() # To get new_notification.notification_id for the log

            # Log the trigger
            new_log = NotificationTriggerLog(
                rule_id=rule.rule_id,
                lease_id=lease.lease_id,
                target_event_date=lease.end_date, # The actual end date of this lease
                notification_id=new_notification.notification_id,
                job_run_id=job_run_id
            )
            db.session.add(new_log)

            current_app.logger.info(f"Scheduled Notification ID {new_notification.notification_id} for Lease ID {lease.lease_id} (Rule ID {rule.rule_id}) to User ID {recipient_user.user_id} via {template.channel.value}.")

    try:
        db.session.commit()
        current_app.logger.info(f"Lease renewal reminder job (ID: {job_run_id}) completed successfully.")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error committing changes for job ID {job_run_id}: {e}", exc_info=True)

if __name__ == '__main__':
    # This is for local testing if you run this file directly.
    # Requires a Flask app context to be pushed.
    # from flask import Flask
    # app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Or your dev DB
    # db.init_app(app)
    # with app.app_context():
    #     # Create tables if needed for testing
    #     # db.create_all()
    #     # Add sample data...
    #     print("Manually running lease renewal job from __main__...")
    #     process_lease_renewal_reminders_job()
    #     print("Manual run finished.")
    pass
