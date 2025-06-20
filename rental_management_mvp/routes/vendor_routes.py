# Placeholder for Vendor (and potentially Staff) specific API Endpoints
# Actual implementation would use a web framework like Flask or FastAPI

# --- Vendor Specific Endpoints (User role: VENDOR) ---

# GET /vendor/jobs (Vendor sees their assigned/available jobs)
def list_vendor_assigned_jobs():
    # TODO: Implement logic for an authenticated VENDOR user to see maintenance requests.
    # Filters: assigned_to_user_id = current_user.id
    # Could also show jobs open for bidding if such a feature exists.
    # Returns a list of MaintenanceRequest details relevant to the vendor.
    pass

# GET /vendor/jobs/{request_id} (Vendor views details of a specific job)
def get_vendor_job_details(request_id: int):
    # TODO: Implement logic for VENDOR to get details of a specific MaintenanceRequest.
    # Ensures the request is assigned to this vendor.
    pass

# POST /vendor/jobs/{request_id}/quote (Vendor submits a quote for a maintenance request)
def submit_maintenance_quote(request_id: int):
    # TODO: Implement logic for VENDOR to submit a quote.
    # Request: { quote_amount, quote_document (file upload), notes (optional) }
    # 1. Uploads quote_document using Document service, gets document_id.
    # 2. Updates MaintenanceRequest:
    #    - vendor_quote_amount
    #    - vendor_quote_document_id
    #    - status to QUOTE_SUBMITTED
    # Triggers notification to Landlord/Staff.
    pass

# POST /vendor/jobs/{request_id}/invoice (Vendor submits an invoice after completing work)
def submit_maintenance_invoice(request_id: int):
    # TODO: Implement logic for VENDOR to submit an invoice.
    # Request: { invoice_amount (optional, if different from quote), invoice_document (file upload), notes (optional) }
    # 1. Uploads invoice_document using Document service, gets document_id.
    # 2. Updates MaintenanceRequest:
    #    - vendor_invoice_document_id
    #    - (Potentially updates status if work was marked RESOLVED by vendor)
    # Triggers notification to Landlord/Staff.
    pass

# PUT /vendor/jobs/{request_id}/status (Vendor updates status of their job)
def update_vendor_job_status(request_id: int):
    # TODO: Implement logic for VENDOR to update status (e.g., IN_PROGRESS, AWAITING_PARTS, RESOLVED).
    # Request: { status, notes (optional) }
    # Ensures vendor is assigned to this request.
    # Updates MaintenanceRequest.status.
    pass


# --- Staff Specific Endpoints (User role: STAFF) ---

# GET /staff/assigned-properties (Staff sees properties they are assigned to manage)
def list_staff_assigned_properties():
    # TODO: Implement logic for an authenticated STAFF user to see properties they manage.
    # Uses User.manages_property_ids.
    pass

# GET /staff/tasks (Staff sees tasks across their assigned properties)
def list_staff_tasks():
    # TODO: Implement logic for STAFF to see tasks.
    # Could include:
    #   - Maintenance requests for their properties.
    #   - Pending application reviews for their properties.
    #   - Lease renewal reminders for their properties.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # Assume User, MaintenanceRequest, Document models are available
#
# vendor_bp = Blueprint('vendor_portal', __name__, url_prefix='/vendor') # For VENDOR role
# staff_bp = Blueprint('staff_portal', __name__, url_prefix='/staff')    # For STAFF role
#
# @vendor_bp.route('/jobs', methods=['GET'])
# def get_jobs_route():
#     # vendor_user = get_current_user() # Ensure role is VENDOR
#     # Call list_vendor_assigned_jobs logic
#     return jsonify([{"request_id": 1, "description": "Fix leaky tap"}]), 200
#
# @vendor_bp.route('/jobs/<int:request_id>/quote', methods=['POST'])
# def submit_quote_route(request_id):
#     # vendor_user = get_current_user()
#     # data = request.form # quote_amount, notes
#     # quote_file = request.files.get('quote_document')
#     # Call submit_maintenance_quote logic
#     return jsonify({"message": "Quote submitted", "request_id": request_id}), 200
#
# @staff_bp.route('/assigned-properties', methods=['GET'])
# def get_assigned_properties_route():
#     # staff_user = get_current_user() # Ensure role is STAFF
#     # Call list_staff_assigned_properties logic
#     return jsonify([{"property_id": 101, "address": "123 Main St"}]), 200
