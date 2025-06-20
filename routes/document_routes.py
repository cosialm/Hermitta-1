# Placeholder for Document Management API Endpoints (Phase 4: Financial Reporting & Advanced Features)
# Actual implementation would use a web framework like Flask or FastAPI

# --- Document Folder Management (Landlord) ---
# POST /document-folders (Landlord creates a new document folder)
def create_document_folder():
    # TODO: Implement logic for an authenticated Landlord to create a document folder.
    # Landlord only (landlord_id from auth token).
    # Request: { name (string), parent_folder_id (optional int, for nesting) }
    # Creates a DocumentFolder record.
    # Response: Full details of the created folder.
    pass

# GET /document-folders (Landlord lists their document folders)
def list_document_folders():
    # TODO: Implement logic for Landlord to list their folder structure.
    # Landlord only.
    # Can be hierarchical (e.g., list root folders, then allow fetching children).
    # Query Params: parent_folder_id (optional, to get subfolders).
    # Response: List of DocumentFolder details.
    pass

# GET /document-folders/{folder_id} (Landlord gets details of a specific folder)
def get_document_folder_details(folder_id: int):
    # TODO: Implement logic for Landlord to get details of a folder.
    # Landlord only, ensures folder belongs to them.
    # May also list documents within this folder (see GET /documents with folder_id filter).
    pass

# PUT /document-folders/{folder_id} (Landlord updates a document folder)
def update_document_folder(folder_id: int):
    # TODO: Implement logic for Landlord to update a folder (e.g., rename, move by changing parent_folder_id).
    # Landlord only.
    # Request: { name (optional string), parent_folder_id (optional int) }
    pass

# DELETE /document-folders/{folder_id} (Landlord deletes a document folder)
def delete_document_folder(folder_id: int):
    # TODO: Implement logic for Landlord to delete a folder.
    # Landlord only.
    # Consider behavior: Delete only if empty? Or delete folder and all contained documents/subfolders (cascade)?
    # Soft delete might be safer for documents.
    pass

# --- Document Management (Landlord, potentially other roles if shared) ---
# POST /documents/upload (Upload a new document)
def upload_document():
    # TODO: Implement logic to upload a new document.
    # Uploader_user_id from authenticated user.
    # Request: Multipart form data for the file.
    # Form data also includes: document_name, document_type (DocumentType enum),
    #                        folder_id (optional FK), tags (optional list of strings),
    #                        expiry_date (optional date), reminder_date_for_expiry (optional date),
    #                        description (optional string),
    #                        # Contextual links (optional, based on where upload happens in UI):
    #                        property_id, lease_id, rental_application_id,
    #                        maintenance_request_id, financial_transaction_id.
    # 1. Securely saves file to storage.
    # 2. Creates a Document record with file_url and all metadata.
    # Response: Full Document details.
    pass

# GET /documents (List/search documents)
def list_documents():
    # TODO: Implement logic to list/search documents.
    # For Landlord: lists documents they uploaded or are linked to their entities.
    # Query Params for filtering:
    #   folder_id, document_type, tags (e.g., ?tags=invoice,tax-2023),
    #   property_id, lease_id, etc. (all FKs on Document model),
    #   uploaded_by_user_id, date_range (for uploaded_at or expiry_date).
    # Supports pagination and sorting.
    pass

# GET /documents/{document_id} (Get specific document metadata)
def get_document_metadata(document_id: int):
    # TODO: Implement logic to get metadata for a specific document.
    # Check permissions (uploader or related entity owner).
    pass

# GET /documents/{document_id}/download (Download the actual file)
def download_document_file(document_id: int):
    # TODO: Implement logic to download the file.
    # Check permissions. Retrieves Document.file_url.
    pass

# PUT /documents/{document_id} (Update document metadata)
def update_document_metadata(document_id: int):
    # TODO: Implement logic to update document metadata.
    # Request: { document_name, description, document_type, folder_id, tags, expiry_date, reminder_date_for_expiry,
    #            contextual FKs if re-linking is allowed }.
    # Check permissions (uploader or related entity owner).
    pass

# DELETE /documents/{document_id} (Delete document)
def delete_document(document_id: int):
    # TODO: Implement logic to delete a document (metadata + file from storage).
    # Check permissions. Soft delete recommended.
    pass

# --- Document Sharing ---
# POST /documents/{document_id}/share (Share a document with another user)
def share_document_with_user(document_id: int):
    # TODO: Implement logic to share a document with another system user.
    # Shared_by_user_id from authenticated user (typically Landlord).
    # Request: { shared_with_user_id, can_view (bool), can_download (bool), expires_at (optional date), access_notes (optional) }
    # Creates a DocumentShare record.
    # May trigger a notification to shared_with_user_id.
    pass

# GET /documents/{document_id}/shares (List who a document is shared with)
def list_document_shares(document_id: int):
    # TODO: Implement logic for document owner to see who it's shared with.
    pass

# PUT /documents/{document_id}/shares/{share_id} (Update a share - e.g., revoke or change expiry)
def update_document_share(document_id: int, share_id: int):
    # TODO: Implement logic to update a specific share record.
    # Request: { can_view, can_download, expires_at } or a specific action like 'revoke'.
    pass

# DELETE /documents/{document_id}/shares/{share_id} (Remove a share)
# Or DELETE /document-shares/{share_id}
def delete_document_share(document_id: int, share_id: int):
    # TODO: Implement logic to stop sharing a document with a user.
    pass

# GET /documents/shared-with-me (User lists documents shared with them)
def list_documents_shared_with_me():
    # TODO: Implement logic for authenticated user to see documents shared with them via DocumentShare.
    pass

# Example (conceptual):
# @doc_bp.route('/folders', methods=['POST']) def create_folder_route(): # ...
# @doc_bp.route('/upload', methods=['POST']) def upload_doc_route(): # ...
# @doc_bp.route('/<int:doc_id>/share', methods=['POST']) def share_doc_route(doc_id): # ...
