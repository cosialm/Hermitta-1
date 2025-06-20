# Placeholder for Landlord Configuration API Endpoints (Phase 2)
# Actual implementation would use a web framework like Flask or FastAPI

# --- Landlord M-Pesa Configuration ---
# POST /landlord/mpesa-configuration (Landlord sets up their M-Pesa API details)
def create_or_update_landlord_mpesa_config():
    # TODO: Implement logic for a landlord to create or update their M-Pesa configuration.
    # Landlord only (landlord_id from authenticated user).
    # Request body should include:
    #   - shortcode_type ('PAYBILL', 'TILL_NUMBER')
    #   - paybill_number (optional)
    #   - till_number (optional)
    #   - consumer_key, consumer_secret, passkey (these should be encrypted before storing)
    #   - account_reference_prefix (optional)
    #   - callback_url_override (optional)
    #   - is_active (boolean)
    # Validates and securely stores the configuration in LandlordMpesaConfiguration model.
    # Might trigger an async validation of credentials with M-Pesa.
    # Response: { config_id, landlord_id, shortcode_type, is_active, validation_status } (omitting sensitive fields).
    pass

# GET /landlord/mpesa-configuration (Landlord views their M-Pesa config)
def get_landlord_mpesa_config():
    # TODO: Implement logic for a landlord to view their M-Pesa configuration.
    # Landlord only.
    # Response: { config_id, landlord_id, shortcode_type, paybill_number (masked/partial),
    #            till_number (masked/partial), is_active, validation_status, account_reference_prefix }
    # IMPORTANT: NEVER return sensitive keys/secrets to the client.
    pass

# POST /landlord/mpesa-configuration/validate (Landlord triggers a validation check for their M-Pesa config)
def validate_landlord_mpesa_config():
    # TODO: Implement logic to trigger a validation of the stored M-Pesa credentials.
    # E.g., by making a balance inquiry or a token generation call to M-Pesa.
    # Updates LandlordMpesaConfiguration.validation_status and last_validation_check.
    # Landlord only.
    # Response: { validation_status, message }
    pass

# --- Landlord Reminder Rules Configuration ---
# POST /landlord/reminder-rules (Landlord creates a new reminder rule)
def create_landlord_reminder_rule():
    # TODO: Implement logic for a landlord to create a reminder rule.
    # Landlord only.
    # Request body: { name, template_id, days_offset, offset_relative_to, send_time_hour, send_time_minute, is_active }
    # Creates a LandlordReminderRule record.
    # Response: Full details of the created rule.
    pass

# GET /landlord/reminder-rules (Landlord lists their reminder rules)
def list_landlord_reminder_rules():
    # TODO: Implement logic for a landlord to list their reminder rules.
    # Landlord only.
    # Supports pagination.
    # Response: List of LandlordReminderRule details.
    pass

# GET /landlord/reminder-rules/{rule_id} (Landlord gets a specific reminder rule)
def get_landlord_reminder_rule_details(rule_id: int):
    # TODO: Implement logic for a landlord to get details of a specific reminder rule.
    # Landlord only, ensures rule belongs to them.
    # Response: Full rule details.
    pass

# PUT /landlord/reminder-rules/{rule_id} (Landlord updates a reminder rule)
def update_landlord_reminder_rule(rule_id: int):
    # TODO: Implement logic for a landlord to update their reminder rule.
    # Landlord only, ensures rule belongs to them.
    # Request body: same fields as create, all optional.
    # Response: Full updated rule details.
    pass

# DELETE /landlord/reminder-rules/{rule_id} (Landlord deletes a reminder rule)
def delete_landlord_reminder_rule(rule_id: int):
    # TODO: Implement logic for a landlord to delete their reminder rule.
    # Landlord only, ensures rule belongs to them.
    # Response: Success message or 204 No Content.
    pass

# (Admin endpoints for managing NotificationTemplate s would be in a separate admin routes file)

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.landlord_mpesa_config import LandlordMpesaConfiguration, MpesaShortcodeType
# # from ..models.landlord_reminder_rule import LandlordReminderRule, ReminderOffsetRelativeTo
#
# landlord_config_bp = Blueprint('landlord_config', __name__, url_prefix='/landlord')
#
# @landlord_config_bp.route('/mpesa-configuration', methods=['POST', 'PUT']) # Create or Update
# def mpesa_config_route():
#     # data = request.get_json()
#     # landlord_id = get_current_user_id()
#     # Securely save/update LandlordMpesaConfiguration
#     return jsonify({"message": "M-Pesa configuration saved", "config_id": 1}), 200
#
# @landlord_config_bp.route('/mpesa-configuration', methods=['GET'])
# def get_mpesa_config_route():
#     # landlord_id = get_current_user_id()
#     # Fetch LandlordMpesaConfiguration, return non-sensitive fields
#     return jsonify({"config_id": 1, "shortcode_type": "PAYBILL", "is_active": True}), 200
#
# @landlord_config_bp.route('/reminder-rules', methods=['POST'])
# def create_reminder_rule_route():
#     # data = request.get_json()
#     # landlord_id = get_current_user_id()
#     # Create LandlordReminderRule
#     return jsonify({"message": "Reminder rule created", "rule_id": 1}), 201
#
# # ... other config routes ...
