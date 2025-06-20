# Placeholder for Financial Transaction (Income/Expense) API Endpoints
# Actual implementation would use a web framework like Flask or FastAPI

# POST /financial-transactions (Landlord records an income or expense)
def record_financial_transaction():
    # TODO: Implement logic for Landlord to record an income or expense.
    # Request: { type: ('INCOME'/'EXPENSE'), category, description, amount, transaction_date,
    #            property_id (optional), lease_id (optional), vendor_name (optional),
    #            related_payment_id (optional) }
    # landlord_id from authenticated user.
    # Creates a FinancialTransaction record.
    # Landlord only.
    pass

# GET /financial-transactions (List transactions for landlord)
def list_financial_transactions():
    # TODO: Implement logic to list financial transactions for the authenticated Landlord.
    # Supports filtering by: property_id, lease_id, type, category, date_range (start_date, end_date).
    # Supports pagination.
    # Landlord only.
    pass

# GET /financial-transactions/{transaction_id} (Get specific transaction)
def get_financial_transaction_details(transaction_id: int):
    # TODO: Implement logic to get details of a specific financial transaction.
    # Ensures transaction belongs to the authenticated Landlord.
    # Landlord only.
    pass

# PUT /financial-transactions/{transaction_id} (Update transaction)
def update_financial_transaction(transaction_id: int):
    # TODO: Implement logic to update an existing financial transaction.
    # Request: { category (optional), description (optional), amount (optional), ... }
    # Ensures transaction belongs to the authenticated Landlord.
    # Landlord only.
    pass

# DELETE /financial-transactions/{transaction_id} (Delete transaction)
def delete_financial_transaction(transaction_id: int):
    # TODO: Implement logic to delete a financial transaction.
    # Ensures transaction belongs to the authenticated Landlord.
    # Landlord only.
    # Consider implications: if it's linked from a Payment, how to handle that? (Soft delete?)
    pass

# POST /financial-transactions/{transaction_id}/upload-receipt (Upload receipt for a transaction)
def upload_transaction_receipt(transaction_id: int):
    # TODO: Implement logic to upload a receipt for a financial transaction.
    # Request: Multipart form data for the receipt file.
    # This will use the Document management system:
    #   1. Uploads the file via Document service (e.g., POST /documents/upload).
    #   2. Gets back the new document_id/file_url.
    #   3. Updates FinancialTransaction.receipt_url (legacy) or links to Document model.
    #      (Preferably, FT model would have a receipt_document_id FK to Document model).
    # Landlord only.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# financial_tx_bp = Blueprint('financial_transactions', __name__, url_prefix='/financial-transactions')
#
# @financial_tx_bp.route('', methods=['POST'])
# def record_transaction_route():
#     # data = request.get_json()
#     # landlord = get_current_user()
#     # Call record_financial_transaction logic
#     return jsonify({"message": "Transaction recorded", "transaction_id": 1}), 201
#
# @financial_tx_bp.route('', methods=['GET'])
# def list_transactions_route():
#     # landlord = get_current_user()
#     # filters = request.args
#     # Call list_financial_transactions logic
#     return jsonify([{"id": 1, "type": "INCOME", "amount": 1200}]), 200
#
# @financial_tx_bp.route('/<int:transaction_id>', methods=['GET'])
# def get_transaction_route(transaction_id):
#     # Call get_financial_transaction_details logic
#     return jsonify({"id": transaction_id, "description": "Rent for March"}), 200
#
# @financial_tx_bp.route('/<int:transaction_id>', methods=['PUT'])
# def update_transaction_route(transaction_id):
#     # data = request.get_json()
#     # Call update_financial_transaction logic
#     return jsonify({"message": "Transaction updated", "transaction_id": transaction_id}), 200
#
# @financial_tx_bp.route('/<int:transaction_id>', methods=['DELETE'])
# def delete_transaction_route(transaction_id):
#     # Call delete_financial_transaction logic
#     return jsonify({"message": "Transaction deleted", "transaction_id": transaction_id}), 200
#
# @financial_tx_bp.route('/<int:transaction_id>/upload-receipt', methods=['POST'])
# def upload_receipt_route(transaction_id):
#     # file = request.files.get('receipt')
#     # Call upload_transaction_receipt logic (which interacts with Document service)
#     return jsonify({"message": "Receipt uploaded for transaction", "transaction_id": transaction_id, "receipt_url": "..."}), 200
