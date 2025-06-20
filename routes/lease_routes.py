# Placeholder for Lease API Endpoints (Phase 3: Enhanced Tenant & Lease Management)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /leases (Landlord creates a lease - can be manual or from application/template)
def create_lease():
    # TODO: Implement logic for a landlord to create a lease.
    # Landlord only.
    # If 'application_id' is provided:
    #   - Pre-fill tenant details from RentalApplication.
    #   - Link lease to application.
    # If 'template_id' is provided (see also /generate-from-template):
    #   - Use LeaseTemplate to populate lease_document_content_final and other fields.
    #   - Landlord provides specific values for placeholders.
    # Else (manual creation):
    #   - Request body includes all necessary fields (property_id, dates, rent, tenant details, etc. as per Phase 1).
    #   - Optional 'lease_document_url' for an initial scanned document (sets version to 1).
    # Sets Lease.signing_status to DRAFT or NOT_STARTED.
    # Response: Full details of the created lease.
    pass

# POST /leases/generate-from-template (Landlord generates a lease draft from a template)
def generate_lease_from_template():
    # TODO: Implement logic for Landlord to generate a lease document from a LeaseTemplate.
    # Landlord only.
    # Request: { template_id, property_id, tenant_id (or tenant_details), start_date, end_date, rent_amount,
    #            security_deposit, other_placeholder_values, custom_clause_inputs (if template allows) }
    # 1. Fetches LeaseTemplate.template_content_body and LeaseTemplate.customizable_clauses_json.
    # 2. Merges/fills placeholders with provided data.
    # 3. Creates a new Lease record with:
    #    - generated_from_template_id = template_id
    #    - lease_document_content_final = (the fully populated lease text/HTML)
    #    - signing_status = DRAFT
    #    - Other lease details (property_id, tenant_id, dates, rent, etc.)
    # Response: { lease_id, lease_document_content_final (for preview), signing_status }
    pass

# GET /leases (List leases)
def list_leases(): # ... (As per Phase 1/2, ensure response includes signing_status)
    pass

# GET /leases/{lease_id} (Get specific lease details)
def get_lease_details(lease_id: int): # ... (As per Phase 1/2, ensure response includes full e-sign fields)
    # Response includes: ... lease_document_content_final, signature_requests, signing_status, signed_lease_document_id.
    pass

# PUT /leases/{lease_id} (Update core lease details - before signing)
def update_lease_core_details(lease_id: int):
    # TODO: Update core details if lease is in DRAFT or NOT_STARTED.
    # If 'lease_document_content_final' is updated, signing process may need to reset.
    pass

# --- E-Signature Workflow (Phase 3) ---
# POST /leases/{lease_id}/initiate-signature (Landlord sends lease for e-signature)
def initiate_lease_e_signature(lease_id: int):
    # TODO: Implement logic to initiate e-signature process for a lease.
    # Landlord only. Lease.signing_status should be DRAFT or NOT_STARTED.
    # Lease.lease_document_content_final must exist.
    # Request: { signers: [ {role: "TENANT", email: "...", name: "..."}, {role: "LANDLORD", email:"...", name:"..."} ],
    #            signature_method_preference: "ESIGN_PROVIDER" / "TYPED_IN_SYSTEM" (optional) }
    # 1. Updates Lease.signature_requests with signer details and status 'PENDING' or 'SENT'.
    # 2. Changes Lease.signing_status to SENT_FOR_SIGNATURE.
    # 3. If using an e-signature provider, makes API call to them with lease_document_content_final (or PDF version).
    #    Stores provider's envelope ID or signer request IDs in Lease.signature_requests.
    # 4. Sends notifications to signers with links to sign (either system link or provider link).
    # Response: Updated Lease.signature_requests and Lease.signing_status.
    pass

# GET /leases/{lease_id}/signing-status (Check current signing status)
def get_lease_signing_status(lease_id: int):
    # TODO: Implement logic to get the current e-signature status and individual signer statuses.
    # Accessible by Landlord and involved Tenant.
    # Response: { lease_id, signing_status, signature_requests }
    pass

# POST /leases/signature/webhook/{provider} (Webhook for external e-signature service - e.g., DocuSign)
def esignature_provider_webhook(provider: str):
    # TODO: Implement logic to handle webhook callbacks from the specified e-signature provider.
    # External, unauthenticated endpoint. IMPORTANT: SECURE THIS (e.g., verify signature from provider).
    # 1. Parses provider payload to identify lease_id/envelope_id and signer events (signed, declined, etc.).
    # 2. Updates corresponding entry in Lease.signature_requests (status, signed_at, ip_address, etc.).
    # 3. Checks if all required signers have signed. If so:
    #    - Updates Lease.signing_status to FULLY_SIGNED_SYSTEM (or similar).
    #    - (Optional) Fetches the signed document from provider and uploads it using the Document service,
    #      then links it via Lease.signed_lease_document_id.
    #    - Triggers notifications.
    # Response: Acknowledgement to the provider.
    pass

# POST /leases/{lease_id}/sign-in-system (A party signs the lease within the system - "typed" signature)
def sign_lease_in_system(lease_id: int):
    # TODO: Implement logic for an authenticated user (Tenant/Landlord) to sign a lease by "typing" their name
    #       or a similar in-system method if not using an external e-signature provider.
    # User must be listed in Lease.signature_requests.
    # Request: { typed_name_signature: "Full Name", consent_checkbox: true }
    # 1. Validates user is a required signer and their turn to sign.
    # 2. Updates their entry in Lease.signature_requests: status to 'SIGNED_SYSTEM', signed_at, ip_address.
    # 3. Checks if all signed; if so, updates Lease.signing_status to FULLY_SIGNED_SYSTEM.
    # 4. Generates a representation of the signed document (e.g., PDF with typed names and audit trail).
    #    This could be stored in Lease.lease_document_url or linked via Lease.signed_lease_document_id.
    # Response: Updated Lease.signature_requests and Lease.signing_status.
    pass

# POST /leases/{lease_id}/upload-signed-copy (Landlord uploads a manually signed lease copy)
def upload_manually_signed_lease_copy(lease_id: int):
    # TODO: Implement logic for Landlord to upload a scanned copy of a lease signed offline.
    # Landlord only.
    # Request: Multipart form data for the document file.
    # 1. Uploads file via Document service, gets document_id.
    # 2. Updates Lease.signed_lease_document_id = new_document_id.
    # 3. Updates Lease.signing_status = FULLY_SIGNED_UPLOADED.
    # 4. Updates Lease.signature_requests to reflect manual signing for all parties (optional detail).
    # Response: Updated lease details.
    pass

# (Legacy/Phase 2 document upload - this is for non-signed/drafts, or if not using e-sign flow)
# POST /leases/{lease_id}/document (Landlord uploads/updates lease draft/unsigned document)
def upload_or_update_lease_draft_document(lease_id: int): # Renamed for clarity
    # TODO: As per Phase 2 - handles draft/unsigned document versioning.
    pass

# GET /leases/{lease_id}/document (Download current draft/unsigned lease document)
def download_current_lease_draft_document(lease_id: int): # Renamed for clarity
    # TODO: As per Phase 2 - downloads the version from lease_document_url.
    pass
