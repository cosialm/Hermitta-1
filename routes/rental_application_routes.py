# Placeholder for Rental Application API Endpoints (Phase 3: Enhanced Tenant & Lease Management)
# Actual implementation would use a web framework like Flask or FastAPI

# --- Applicant Facing Endpoints ---
# POST /rental-applications (Applicant submits an application for a property)
def submit_rental_application():
    # TODO: Implement logic for an applicant to submit/update their application (can be multi-step).
    # Request: { property_id, full_name, email, phone_number,
    #            application_data (JSON with standard fields like income, employment),
    #            custom_fields_data (JSON with answers to landlord's custom questions),
    #            applicant_consent_data_processing (boolean),
    #            applicant_consent_background_check (boolean),
    #            notes_for_landlord (optional string) }
    # If applicant is logged in, applicant_user_id can be pre-filled.
    # Creates/updates a RentalApplication record. Status could be DRAFT initially, then SUBMITTED.
    # If LandlordApplicationConfig specifies an application_fee, status might go to AWAITING_FEE_PAYMENT.
    # Response: { application_id, status, next_step (if any) }.
    pass

# GET /rental-applications/my (Applicant views their submitted applications)
def list_my_applications():
    # TODO: Implement logic for an authenticated applicant to list their applications.
    # Filters by applicant_user_id.
    # Response: List of RentalApplication summaries (id, property_address, status, submitted_at).
    pass

# GET /rental-applications/{application_id}/my-details (Applicant views their specific application)
def get_my_application_details(application_id: int):
    # TODO: Implement logic for applicant to view their specific application.
    # Ensures application belongs to the authenticated applicant.
    # Response: Full RentalApplication details.
    pass

# POST /rental-applications/{application_id}/documents (Applicant uploads a document for their application)
def upload_application_document(application_id: int):
    # TODO: Implement logic for an applicant to upload a supporting document.
    # Applicant only, for their own application.
    # Request: Multipart form data with file, and 'document_type' (from ApplicationDocumentType enum).
    # Creates an ApplicationDocument record linked to the application_id.
    # Response: Details of the uploaded ApplicationDocument.
    pass

# GET /rental-applications/{application_id}/documents (Applicant lists their uploaded documents)
def list_my_application_documents(application_id: int):
    # TODO: Implement logic for an applicant to list documents they uploaded for an application.
    # Applicant only.
    # Response: List of ApplicationDocument details.
    pass

# DELETE /rental-applications/{application_id}/documents/{app_doc_id} (Applicant deletes an uploaded document)
def delete_my_application_document(application_id: int, app_doc_id: int):
    # TODO: Implement logic for an applicant to delete a document they uploaded.
    # Applicant only, ensures document belongs to their application. Status of application might restrict this.
    # Deletes ApplicationDocument record and the file from storage.
    pass

# PUT /rental-applications/{application_id}/withdraw (Applicant withdraws their application)
def withdraw_my_application(application_id: int):
    # TODO: Implement logic for an applicant to withdraw their application.
    # Updates RentalApplication.status to WITHDRAWN.
    # Applicant only, for their own application, if status allows withdrawal (e.g., not already APPROVED/REJECTED).
    pass

# --- Landlord Facing Endpoints ---
# GET /landlord/properties/{property_id}/applications (Landlord views applications for a specific property)
def list_applications_for_property(property_id: int):
    # TODO: Implement logic for Landlord to list applications for one of their properties.
    # Landlord only, ensures property belongs to them.
    # Filters: status, date range. Pagination.
    # Response: List of RentalApplication summaries.
    pass

# GET /landlord/applications (Landlord views all applications for their properties)
def list_all_landlord_applications():
    # TODO: Implement logic for Landlord to list all applications across all their properties.
    # Landlord only. Filters: status, property_id, date range. Pagination.
    pass

# GET /landlord/applications/{application_id} (Landlord views specific application details)
def get_landlord_application_view(application_id: int):
    # TODO: Implement logic for Landlord to get full details of an application.
    # Landlord only, ensures application is for one of their properties.
    # Response: Full RentalApplication details, including ApplicationDocument list.
    pass

# PUT /landlord/applications/{application_id}/status (Landlord updates application status)
def update_application_status_by_landlord(application_id: int):
    # TODO: Implement logic for Landlord to update an application's status.
    # Request: { status: ('UNDER_REVIEW', 'AWAITING_DOCUMENTS', 'APPROVED', 'REJECTED'), internal_notes (optional) }
    # Updates RentalApplication.status, RentalApplication.reviewed_at (if applicable), RentalApplication.internal_notes.
    # May trigger notifications to applicant.
    pass

# POST /landlord/applications/{application_id}/notes (Landlord adds/updates internal notes)
def update_application_internal_notes(application_id: int):
    # TODO: Implement logic for Landlord to add/update internal notes.
    # Request: { internal_notes: "text" }
    pass

# --- Landlord Application Configuration (Optional Advanced Feature) ---
# POST /landlord/application-configuration (Landlord defines custom application fields)
def set_landlord_application_config():
    # TODO: Implement logic for landlord to set their custom application field definitions.
    # Request: { custom_field_definitions (JSON array), application_fee (optional) }
    # Creates/Updates LandlordApplicationConfig record.
    pass

# GET /landlord/application-configuration (Landlord retrieves their custom application config)
def get_landlord_application_config():
    # TODO: Implement logic for landlord to get their LandlordApplicationConfig.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# rental_app_bp = Blueprint('rental_applications_public', __name__, url_prefix='/rental-applications') # Applicant facing
# landlord_rental_app_bp = Blueprint('rental_applications_landlord', __name__, url_prefix='/landlord') # Landlord facing
#
# @rental_app_bp.route('', methods=['POST'])
# def submit_app_route(): # ...
#     return jsonify({"message": "Application submitted", "application_id": 1}), 201
#
# @landlord_rental_app_bp.route('/applications/<int:application_id>/status', methods=['PUT'])
# def update_app_status_route(application_id): # ...
#     return jsonify({"message": "Application status updated"}), 200
