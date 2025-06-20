# Placeholder for Maintenance Request API Endpoints (Phase 3: Enhanced Tenant & Lease Management)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /maintenance-requests (Tenant submits a new request)
def submit_maintenance_request():
    # TODO: Implement logic for a tenant to submit a new maintenance request.
    # Tenant only.
    # Request: { property_id, description, category (MaintenanceRequestCategory),
    #            priority (optional, MaintenancePriority), tenant_contact_preference (optional),
    #            initial_photo_files (optional, multipart files for MaintenanceAttachment) }
    # 1. Creates MaintenanceRequest record (status SUBMITTED, priority if provided).
    # 2. If initial_photo_files are present, uploads them and creates MaintenanceAttachment records linked to the request.
    #    Updates MaintenanceRequest.initial_photo_urls (or relies on attachments being listed separately).
    # Response: Full details of the created MaintenanceRequest, including any created attachment metadata.
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
    #           MaintenanceAttachment records and MaintenanceCommunication records (excluding internal notes for tenant/vendor).
    pass

# PUT /maintenance-requests/{request_id} (Update request - typically by Landlord/Staff/Vendor)
def update_maintenance_request(request_id: int):
    # TODO: Implement logic for Landlord/Staff/Vendor to update a maintenance request.
    # Permissions vary by role:
    #   - Landlord/Staff: can update status, priority, assigned_to_user_id, assigned_vendor_name_manual,
    #                     scheduled_date, resolution_notes, actual_cost, resolved_by_user_id.
    #   - Assigned Vendor (if system user): can update status (e.g., IN_PROGRESS, RESOLVED_BY_ASSIGNED_PARTY), resolution_notes.
    # Request: { status, priority, assigned_to_user_id, assigned_vendor_name_manual, scheduled_date,
    #            resolution_notes, actual_cost, resolved_by_user_id } (all optional).
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
    # Request: { message_text, is_internal_note (boolean, only for Landlord/Staff) }
    # Creates MaintenanceCommunication record.
    # If not is_internal_note, may trigger notification to other parties on the request.
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
