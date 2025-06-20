# Placeholder for Maintenance Request API Endpoints (Refined for Phase 1 MVP - Basic)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /maintenance-requests (Tenant submits a new request)
def submit_maintenance_request():
    # TODO: Implement logic for a tenant to submit a new maintenance request.
    # Tenant only (tenant_id from authenticated user).
    # Request body should include:
    #   - property_id (must be a property associated with the tenant's current lease)
    #   - description (text detailing the issue)
    #   - category (from MaintenanceRequestCategory enum, e.g., "PLUMBING", "ELECTRICAL")
    #   - tenant_contact_preference (Optional string, e.g., "Call before coming", "SMS me updates")
    # Creates a MaintenanceRequest record with status SUBMITTED.
    # Response: Full details of the created maintenance request.
    pass

# GET /maintenance-requests (List maintenance requests)
def list_maintenance_requests():
    # TODO: Implement logic to list maintenance requests.
    # If authenticated user is Tenant: lists requests they submitted.
    # If authenticated user is Landlord: lists requests for properties they own.
    #   - Supports filtering by property_id, status.
    # Supports pagination.
    # Response: List of maintenance request summaries.
    pass

# GET /maintenance-requests/{request_id} (Get specific request details)
def get_maintenance_request_details(request_id: int):
    # TODO: Implement logic to get details of a specific maintenance request.
    # Accessible by the Tenant who submitted it or the Landlord who owns the related property.
    # Response: Full maintenance request details.
    pass

# PUT /maintenance-requests/{request_id} (Landlord updates request status)
def update_maintenance_request_status(request_id: int):
    # TODO: Implement logic for a landlord to update the status of a maintenance request.
    # Landlord only, for requests on their properties.
    # Request body should include:
    #   - status (from MaintenanceRequestStatus enum, e.g., "IN_PROGRESS", "RESOLVED", "CLOSED")
    #   - (Optional) resolution_notes when moving to RESOLVED or CLOSED.
    # Updates MaintenanceRequest.status, MaintenanceRequest.updated_at.
    # If status is RESOLVED, MaintenanceRequest.resolved_at is set.
    # Response: Full updated maintenance request details.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.maintenance_request import MaintenanceRequest, MaintenanceRequestCategory, MaintenanceRequestStatus
#
# maintenance_bp = Blueprint('maintenance', __name__, url_prefix='/maintenance-requests')
#
# @maintenance_bp.route('', methods=['POST'])
# def submit_request_route():
#     # data = request.get_json()
#     # tenant_id = get_current_user_id()
#     # Create MaintenanceRequest object with property_id, description, category, tenant_contact_preference.
#     # request.tenant_id = tenant_id
#     # request.save()
#     return jsonify({"message": "Maintenance request submitted", "request_id": 1, "details": "{...}"}), 201
#
# @maintenance_bp.route('', methods=['GET'])
# def list_requests_route():
#     # user = get_current_user()
#     # if user.role == UserRole.TENANT:
#     #    requests = MaintenanceRequest.query.filter_by(tenant_id=user.id).all()
#     # elif user.role == UserRole.LANDLORD:
#     #    # Logic to get requests for landlord's properties
#     #    requests = []
#     return jsonify([{"id": r.id, "description": r.description, "status": r.status.value} for r in []]), 200 # Placeholder
#
# @maintenance_bp.route('/<int:request_id>', methods=['PUT'])
# def update_request_route(request_id):
#     # data = request.get_json() # { status, resolution_notes (optional) }
#     # landlord_id = get_current_user_id()
#     # Fetch request, check ownership/permissions.
#     # Update request status, resolved_at if applicable.
#     # request.save()
#     return jsonify({"message": "Request status updated", "request_id": request_id, "details": "{...}"}), 200
