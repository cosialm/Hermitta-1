# Placeholder for Notification API Endpoints (Phase 2: Online Payments & Communication)
# Actual implementation would use a web framework like Flask or FastAPI

# GET /notifications (Get notifications for the logged-in user)
def get_user_notifications():
    # TODO: Implement logic to retrieve notifications for the authenticated user from Notification model.
    # Supports pagination (e.g., ?page=1&limit=10).
    # Filters can be added (e.g., ?status=READ/UNREAD (derived from read_at), ?type=RENT_REMINDER).
    # Response should include: notification_id, type, content (if pre-generated, or a summary),
    # delivery_method, status (e.g. SENT_SUCCESS, DELIVERY_CONFIRMED, READ), sent_at, read_at,
    # related_entity_type, related_entity_id.
    pass

# POST /notifications/{notification_id}/mark-read (Mark a notification as read)
def mark_notification_as_read(notification_id: int):
    # TODO: Implement logic to mark a specific notification as read.
    # Primarily for IN_APP notifications. Updates Notification.read_at and Notification.status to READ.
    # Ensures the notification belongs to the authenticated user.
    # Response: Updated notification details or success status.
    pass

# POST /notifications/mark-all-read (Mark all unread notifications as read for the user)
def mark_all_notifications_as_read():
    # TODO: Implement logic to mark all unread IN_APP notifications as read for the authenticated user.
    # Updates Notification.read_at and Notification.status for relevant notifications.
    # Response: Success status, count of messages marked read.
    pass

# System Processes (Background tasks, not direct API endpoints, but crucial for Phase 2 notifications):
# - Notification Scheduler (Cron Job):
#   - Periodically queries LandlordReminderRule entries that are active.
#   - For each rule, determines relevant leases and users (tenants, landlords based on User.preferred_language).
#   - Calculates scheduled_send_time based on rule's offset (e.g., 7 days before rent_due_date).
#   - Creates Notification records with status SCHEDULED, linking to user_id, lease_id, template_id,
#     reminder_rule_id, and template_context (e.g., tenant_name, rent_amount, due_date).
#
# - Notification Dispatcher (Background Worker):
#   - Periodically queries Notification records with status SCHEDULED and scheduled_send_time in the past,
#     OR records with status PENDING_SEND.
#   - For each notification:
#     1. Retrieves NotificationTemplate using template_id from Notification.
#     2. Selects language (EN/SW) based on User.preferred_language for the recipient.
#     3. Populates the template's subject/body with data from Notification.template_context. The result is the final 'content'.
#     4. Dispatches the notification (final 'content') via the specified delivery_method (EMAIL, SMS, IN_APP).
#        - For EMAIL/SMS, integrates with external gateways (e.g., SendGrid, Twilio, Africa's Talking).
#        - For IN_APP, simply stores it (content + metadata) for retrieval by the user's client.
#     5. Updates Notification status to SENT_SUCCESS or SENT_FAIL (with error_message).
#     6. Optionally, listens for delivery confirmation webhooks from gateways to update status to
#        DELIVERY_CONFIRMED or DELIVERY_FAILED.
#
# - Event-Driven Notification Creation:
#   - Other system events (e.g., M-Pesa payment success/failure, new message received) directly create
#     Notification records with status PENDING_SEND (or SCHEDULED if for immediate dispatch by worker),
#     providing template_id and context. The Dispatcher then picks these up.

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.notification import Notification, NotificationStatus, NotificationType
#
# notification_bp = Blueprint('notifications', __name__, url_prefix='/notifications')
#
# @notification_bp.route('', methods=['GET'])
# def get_user_notifications_route():
#     # user = get_current_user()
#     # Call get_user_notifications logic for this user
#     # Example response item: {"notification_id": 1, "type": "RENT_REMINDER", "status": "SENT_SUCCESS",
#     #                        "content_preview": "Dear John, your rent is due...", "sent_at": "..."}
#     return jsonify([]), 200
#
# @notification_bp.route('/<int:notification_id>/mark-read', methods=['POST'])
# def mark_read_route(notification_id):
#     # user = get_current_user()
#     # Call mark_notification_as_read logic
#     return jsonify({"message": "Notification marked as read", "notification_id": notification_id}), 200
#
# @notification_bp.route('/mark-all-read', methods=['POST'])
# def mark_all_read_route():
#     # user = get_current_user()
#     # Call mark_all_notifications_as_read logic
#     return jsonify({"message": "All notifications marked as read"}), 200
