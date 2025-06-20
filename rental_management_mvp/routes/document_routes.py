# Placeholder for Document Management API Endpoints
# Actual implementation would use a web framework like Flask or FastAPI

# POST /documents/upload (Upload a new document)
def upload_document():
    # TODO: Implement logic to upload a new document.
    # Request: Multipart form data for the file.
    # Form data also includes: document_name, document_type,
    #                        property_id (optional), lease_id (optional),
    #                        rental_application_id (optional), maintenance_request_id (optional),
    #                        financial_transaction_id (optional), description (optional).
    # uploader_user_id from authenticated user.
    # 1. Securely saves the file to a storage service (e.g., S3, local filestore).
    # 2. Creates a Document record with file_url and other metadata.
    # Response: { document_id, file_url, document_name, ... }
    pass

# GET /documents (List documents)
def list_documents():
    # TODO: Implement logic to list documents for the authenticated user.
    # User can only see documents they uploaded or are related to their context
    # (e.g., documents for their properties, leases, applications).
    # Query Params for filtering:
    #   - property_id
    #   - lease_id
    #   - rental_application_id
    #   - maintenance_request_id
    #   - financial_transaction_id
    #   - document_type
    #   - uploader_user_id (for admins, or if users can see docs uploaded by others in same context)
    #   - date_range (uploaded_at)
    # Supports pagination.
    pass

# GET /documents/{document_id} (Get specific document metadata)
def get_document_metadata(document_id: int):
    # TODO: Implement logic to get metadata for a specific document.
    # Ensures user has permission to access this document.
    # Does NOT return the file itself, just its metadata.
    pass

# GET /documents/{document_id}/download (Download the actual file)
def download_document_file(document_id: int):
    # TODO: Implement logic to download the actual file of a document.
    # Ensures user has permission.
    # Retrieves Document.file_url and streams the file or redirects to it.
    # Needs appropriate headers (Content-Disposition, Content-Type).
    pass

# PUT /documents/{document_id} (Update document metadata)
def update_document_metadata(document_id: int):
    # TODO: Implement logic to update metadata of a document.
    # Request: { document_name (optional), description (optional), document_type (optional),
    #            property_id (optional), lease_id (optional), ... (ability to re-link) }
    # Ensures user has permission (typically uploader or landlord in context).
    # Does NOT allow changing the file itself via this endpoint.
    pass

# DELETE /documents/{document_id} (Delete document file and metadata)
def delete_document(document_id: int):
    # TODO: Implement logic to delete a document.
    # Ensures user has permission.
    # 1. Deletes the file from storage.
    # 2. Deletes the Document record.
    # Consider soft delete vs hard delete policies.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify, send_from_directory
# document_bp = Blueprint('documents', __name__, url_prefix='/documents')
#
# @document_bp.route('/upload', methods=['POST'])
# def upload_document_route():
#     # file = request.files.get('file')
#     # form_data = request.form
#     # user = get_current_user()
#     # Call upload_document logic
#     return jsonify({"message": "Document uploaded", "document_id": 1, "file_url": "..."}), 201
#
# @document_bp.route('', methods=['GET'])
# def list_documents_route():
#     # user = get_current_user()
#     # filters = request.args
#     # Call list_documents logic
#     return jsonify([{"id": 1, "name": "Lease.pdf", "type": "LEASE_AGREEMENT"}]), 200
#
# @document_bp.route('/<int:document_id>', methods=['GET'])
# def get_metadata_route(document_id):
#     # Call get_document_metadata logic
#     return jsonify({"id": document_id, "name": "Lease.pdf", "uploaded_at": "..."}), 200
#
# @document_bp.route('/<int:document_id>/download', methods=['GET'])
# def download_file_route(document_id):
#     # Call download_document_file logic to get file path/stream
#     # Example: return send_from_directory('path/to/files', 'filename.pdf')
#     return jsonify({"message": "Download initiated (placeholder)"}), 200 # Placeholder
#
# @document_bp.route('/<int:document_id>', methods=['PUT'])
# def update_metadata_route(document_id):
#     # data = request.get_json()
#     # Call update_document_metadata logic
#     return jsonify({"message": "Document metadata updated", "document_id": document_id}), 200
#
# @document_bp.route('/<int:document_id>', methods=['DELETE'])
# def delete_document_route(document_id):
#     # Call delete_document logic
#     return jsonify({"message": "Document deleted", "document_id": document_id}), 200
