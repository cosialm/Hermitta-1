# Placeholder for Maintenance Request API Endpoints (Phase 3: Enhanced Tenant & Lease Management)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /maintenance-requests (Tenant submits a new request)
def submit_maintenance_request():
    # TODO: Implement logic for a tenant or landlord/staff to submit a new maintenance request.
    # Tenant/Landlord/Staff.
    # Request: { property_id, description, category (MaintenanceRequestCategory),
    #            priority (optional, MaintenancePriority), tenant_contact_preference (optional),
    #            initial_photo_files (optional, multipart files for MaintenanceAttachment),
    #            assigned_vendor_ids: Optional[List[int]] (New: list of vendor User IDs to assign)
    #          }
    # 1. Creates MaintenanceRequest record (status SUBMITTED or PENDING_VENDOR_ASSIGNMENT if vendors assigned).
    # 2. If initial_photo_files are present, uploads them and creates MaintenanceAttachment records.
    # 3. If assigned_vendor_ids are provided:
    #    a. For each vendor_id, create a MaintenanceRequestVendorAssignment record
    #       (request_id from new request, vendor_id, status=PENDING_ACCEPTANCE).
    #    b. The MaintenanceRequest.assigned_to_user_id could be set to the first vendor_id or remain null if multiple.
    #       The overall request status might become AWAITING_VENDOR_ACCEPTANCE.
    # Response: Full details of the created MaintenanceRequest, including any created attachment metadata and assignment info.
    pass

# GET /maintenance-requests (List maintenance requests)
def list_maintenance_requests():
    # TODO: Implement logic to list maintenance requests.
    # For Tenant: lists their submitted requests.
    # For Landlord/Staff: lists requests for their assigned/owned properties.
    # Filters: property_id, status, priority, category, assigned_to_user_id, date_range. Pagination.
    # Response: List of MaintenanceRequest summaries.
    pass

# GET /maintenance-requests/{request_id} (Get specific request details)
def get_maintenance_request_details(request_id: int):
    # TODO: Implement logic to get full details of a specific maintenance request.
    # Accessible by Tenant who submitted, Landlord of property, or assigned Staff/Vendor.
    # Response: Full MaintenanceRequest details, including lists of associated
    #           MaintenanceAttachment records, MaintenanceCommunication records (excluding internal notes for tenant/vendor),
    #           and a list of MaintenanceRequestVendorAssignment details (vendor_id, status, assigned_at, quote_id).
    pass

# PUT /maintenance-requests/{request_id} (Update core request details - typically by Landlord/Staff/Vendor)
def update_maintenance_request(request_id: int):
    # TODO: Implement logic for Landlord/Staff/Vendor to update a maintenance request.
    # Note: Assigning/unassigning vendors is preferably handled via dedicated assignment endpoints.
    #       This endpoint would handle changes to core fields like description, priority, overall status,
    #       scheduled_date, resolution_notes, actual_cost, resolved_by_user_id.
    #       Updating assigned_to_user_id here would be for the 'primary' or 'winning' vendor after quote approval.
    # Permissions vary by role:
    #   - Landlord/Staff: can update status, priority, scheduled_date, resolution_notes, actual_cost, resolved_by_user_id.
    #                     Can also update the primary assigned_to_user_id (e.g., after quote approval).
    #   - Assigned Vendor (if system user, via their specific assignment): can update status of their assignment (see maintenance_assignment_routes).
    # Request: { status, priority, description, scheduled_date, resolution_notes, actual_cost, resolved_by_user_id,
    #            assigned_to_user_id (for primary vendor) } (all optional).
    # Updates relevant fields in MaintenanceRequest. Sets timestamps like acknowledged_at, resolved_at, closed_at.
    # Response: Full updated MaintenanceRequest details.
    pass

# --- Maintenance Attachments ---
# POST /maintenance-requests/{request_id}/attachments (Upload an attachment to a request)
def add_maintenance_attachment(request_id: int):
    # TODO: Implement logic for Tenant, Landlord, Staff, or Vendor to add an attachment.
    # Authenticated user with access to the request.
    # Request: Multipart form data for file, 'file_type' (MaintenanceAttachmentFileType), 'description' (optional).
    # Creates MaintenanceAttachment record linked to request_id and uploader_user_id.
    # Response: Details of the created MaintenanceAttachment.
    pass

# GET /maintenance-requests/{request_id}/attachments (List attachments for a request)
def list_maintenance_attachments(request_id: int):
    # TODO: Implement logic to list attachments for a maintenance request.
    # Accessible by users with access to the request.
    # Response: List of MaintenanceAttachment details.
    pass

# DELETE /maintenance-requests/{request_id}/attachments/{attachment_id} (Delete an attachment)
def delete_maintenance_attachment(request_id: int, attachment_id: int):
    # TODO: Implement logic to delete an attachment.
    # Uploader or Landlord/Staff with permissions.
    # Deletes MaintenanceAttachment record and file from storage.
    pass

# --- Maintenance Communication ---
# POST /maintenance-requests/{request_id}/communications (Add a message/note to a request)
def add_maintenance_communication(request_id: int):
    # TODO: Implement logic to add a communication entry to a maintenance request.
    # Authenticated user with access to the request (Tenant, Landlord, Staff, Vendor).
    # Request: { message_text, is_internal_note (boolean, only for Landlord/Staff),
    #            recipient_vendor_id: Optional[int] (if message is for a specific assigned vendor) }
    # Creates MaintenanceCommunication record.
    # If not is_internal_note, may trigger notification to other parties on the request
    # (e.g., tenant, all assigned vendors if recipient_vendor_id is null, or specific vendor).
    # Response: Details of the created MaintenanceCommunication.
    pass

# GET /maintenance-requests/{request_id}/communications (List communications for a request)
def list_maintenance_communications(request_id: int):
    # TODO: Implement logic to list communications for a maintenance request.
    # Filters out is_internal_note=true for Tenants/Vendors.
    # Accessible by users with access to the request. Pagination.
    # Response: List of MaintenanceCommunication details.
    pass

# --- Tenant Feedback ---
# POST /maintenance-requests/{request_id}/feedback (Tenant submits feedback after resolution)
def submit_maintenance_feedback(request_id: int):
    # TODO: Implement logic for a Tenant to submit feedback on a resolved maintenance request.
    # Tenant only, for their own requests, if status is PENDING_TENANT_CONFIRMATION or COMPLETED_CONFIRMED_BY_TENANT.
    # Request: { tenant_feedback_rating (int 1-5), tenant_feedback_comment (optional string) }
    # Updates MaintenanceRequest with feedback fields. Can change status to COMPLETED_CONFIRMED_BY_TENANT.
    # Response: Updated MaintenanceRequest details.
    pass

# Example (conceptual):
# @maintenance_bp.route('/<int:request_id>/attachments', methods=['POST'])
# def add_attachment_route(request_id): # ...
#     return jsonify({"message": "Attachment added", "attachment_id": 1}), 201
#
# @maintenance_bp.route('/<int:request_id>/communications', methods=['POST'])
# def add_comm_route(request_id): # ...
#     return jsonify({"message": "Communication added", "comm_id": 1}), 201
#
# @maintenance_bp.route('/<int:request_id>/feedback', methods=['POST'])
# def submit_feedback_route(request_id): # ...
#     return jsonify({"message": "Feedback submitted"}), 200
