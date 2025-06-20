# Placeholder for Maintenance Request Vendor Assignment API Endpoints
# Actual implementation would use a web framework like Flask or FastAPI

# from ..models.maintenance_request_vendor_assignment import MaintenanceRequestVendorAssignment, VendorAssignmentStatus
# from ..models.user import UserRole # To check if user is VENDOR
# from ..services.notification_service import send_notification # Conceptual

# POST /maintenance-requests/{request_id}/assignments (Assign vendor(s) to a request)
def assign_vendors_to_maintenance_request(request_id: int):
    # TODO: Implement logic to assign one or more vendors to a maintenance request.
    # Typically Landlord/Staff.
    # Request Body: { vendor_ids: List[int], vendor_specific_instructions: Optional[str] }
    # 1. Authorize user.
    # 2. For each vendor_id in vendor_ids:
    #    a. Check if vendor exists and has VENDOR role.
    #    b. Check if vendor is already assigned to this request (to avoid duplicates or handle re-assignment).
    #    c. Create MaintenanceRequestVendorAssignment record:
    #       - request_id = request_id
    #       - vendor_id = vendor_id
    #       - status = VendorAssignmentStatus.PENDING_ACCEPTANCE
    #       - vendor_specific_instructions (if provided globally for this batch)
    #    d. Optionally, send notification to vendor about the new assignment.
    #       (e.g., send_notification(vendor_id, template="NEW_MAINTENANCE_ASSIGNMENT", context={request_id: ...}))
    # 3. Update overall MaintenanceRequest status if needed (e.g., to AWAITING_VENDOR_ACCEPTANCE).
    # Response: List of created MaintenanceRequestVendorAssignment details or success message.
    pass

# GET /maintenance-requests/{request_id}/assignments (List assignments for a request)
def list_assignments_for_maintenance_request(request_id: int):
    # TODO: Implement logic to list all vendor assignments for a specific maintenance request.
    # Accessible by Landlord/Staff, and potentially assigned Vendors (to see their own or co-assignments).
    # 1. Authorize user.
    # 2. Fetch all MaintenanceRequestVendorAssignment records where request_id = request_id.
    # 3. Response: List of MaintenanceRequestVendorAssignment details (including vendor info, status, quote_id).
    pass

# GET /maintenance-assignments/{assignment_id} (Get details of a specific assignment)
def get_maintenance_assignment_details(assignment_id: int):
    # TODO: Implement logic to get details of a specific vendor assignment.
    # Accessible by Landlord/Staff, and the assigned Vendor.
    # 1. Authorize user.
    # 2. Fetch MaintenanceRequestVendorAssignment by assignment_id.
    # 3. Response: Full MaintenanceRequestVendorAssignment details.
    pass

# PUT /maintenance-assignments/{assignment_id} (Update a vendor assignment - e.g., vendor accepts/declines)
def update_maintenance_assignment(assignment_id: int):
    # TODO: Implement logic for a vendor to update their assignment status, or landlord to modify details.
    # Permissions vary by role:
    #   - Assigned Vendor: Can update status (e.g., PENDING_ACCEPTANCE -> ACCEPTED or DECLINED).
    #                    Can link their vendor_quote_id.
    #   - Landlord/Staff: Can update status (e.g., CANCELLED_BY_LANDLORD), vendor_specific_instructions.
    # Request Body: { status: VendorAssignmentStatus (e.g. "ACCEPTED", "DECLINED"), vendor_quote_id: Optional[int] }
    # 1. Authorize user (is it the assigned vendor? or landlord/staff for this request?).
    # 2. Fetch MaintenanceRequestVendorAssignment by assignment_id.
    # 3. Perform validation based on current status and user role (e.g., vendor can't set to CANCELLED_BY_LANDLORD).
    # 4. Update status and relevant timestamps (e.g., accepted_at, declined_at).
    # 5. If vendor accepts/declines, or landlord cancels, notify other relevant parties.
    #    (e.g., landlord notified if vendor accepts/declines).
    # 6. Update overall MaintenanceRequest status if necessary (e.g., if all vendors decline, back to PENDING_VENDOR_ASSIGNMENT).
    # Response: Full updated MaintenanceRequestVendorAssignment details.
    pass

# DELETE /maintenance-assignments/{assignment_id} (Remove/cancel a specific vendor assignment)
# This is effectively covered by PUT with status=CANCELLED_BY_LANDLORD if initiated by landlord,
# or status=DECLINED if by vendor. A hard delete might be an admin action.
# For simplicity, we can assume "cancelling" is done via PUT to change status.
# If a true DELETE is needed:
# def delete_maintenance_assignment(assignment_id: int):
#     # TODO: Implement logic to hard delete a vendor assignment (use with caution).
#     # Typically Landlord/Staff, perhaps only if assignment is in PENDING_ACCEPTANCE.
#     # 1. Authorize user.
#     # 2. Fetch MaintenanceRequestVendorAssignment.
#     # 3. Business rule: e.g., can only delete if no work started, no quote submitted.
#     # 4. Delete the record.
#     # 5. Notify vendor if they were not the initiator.
#     # Response: Success message or 204 No Content.
#     pass

# --- Quote Management with Multiple Vendors ---
# When a vendor (linked via MaintenanceRequestVendorAssignment) submits a quote:
# - The Quote model should store `request_id` and `vendor_id`.
# - The `update_maintenance_assignment` endpoint can be used by the vendor to set `vendor_quote_id` on their assignment.
# - The Landlord, when viewing a MaintenanceRequest, would see all assignments and their linked quotes.
# - When the Landlord approves a specific Quote:
#   1. The approved Quote's status is updated.
#   2. The corresponding MaintenanceRequestVendorAssignment status might change to WORK_IN_PROGRESS or similar.
#   3. The main MaintenanceRequest.status changes to QUOTE_APPROVED_BY_LANDLORD.
#   4. MaintenanceRequest.quote_id (the top-level one) is set to the ID of the approved quote.
#   5. Other vendors' assignments for the same request might have their status updated (e.g., to 'QUOTE_NOT_SELECTED' - new status for assignment?).

# Example (conceptual Flask routes):
# from flask import Blueprint, request, jsonify
# maintenance_assignment_bp = Blueprint('maintenance_assignments', __name__)
#
# @maintenance_assignment_bp.route('/maintenance-requests/<int:request_id>/assignments', methods=['POST'])
# def assign_vendors_route(request_id):
#     # data = request.get_json() # { vendor_ids: [1,2,3] }
#     # ... call assign_vendors_to_maintenance_request logic ...
#     return jsonify({"message": "Vendors assigned"}), 201
#
# @maintenance_assignment_bp.route('/maintenance-assignments/<int:assignment_id>', methods=['PUT'])
# def update_assignment_route(assignment_id):
#     # data = request.get_json() # { status: "ACCEPTED" }
#     # ... call update_maintenance_assignment logic ...
#     return jsonify({"message": "Assignment updated"}), 200
