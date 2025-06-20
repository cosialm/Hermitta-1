# Placeholder for Financial Transaction API Endpoints (Phase 4: Financial Reporting & Advanced Features)
# Actual implementation would use a web framework like Flask or FastAPI

# --- User Financial Category Management (Landlord) ---
# POST /financial-categories (Landlord creates a custom financial category)
def create_user_financial_category():
    # TODO: Implement logic for Landlord to create a custom income/expense category.
    # Landlord only (landlord_id from authenticated user).
    # Request: { name (string), type ('INCOME'/'EXPENSE'), description (optional string) }
    # Creates a UserFinancialCategory record. is_system_default will be False.
    # Response: Full details of the created category.
    pass

# GET /financial-categories (Landlord lists their custom categories + system defaults)
def list_user_financial_categories():
    # TODO: Implement logic for Landlord to list their categories.
    # Landlord only.
    # Returns list of UserFinancialCategory where landlord_id is current user OR landlord_id is NULL (system defaults).
    # Filter by type ('INCOME'/'EXPENSE').
    pass

# PUT /financial-categories/{category_id} (Landlord updates their custom category)
def update_user_financial_category(category_id: int):
    # TODO: Implement logic for Landlord to update their custom category.
    # Landlord only, ensures category belongs to them and is_system_default is False.
    # Request: { name (optional), description (optional) } (Type cannot be changed).
    pass

# DELETE /financial-categories/{category_id} (Landlord deletes their custom category)
def delete_user_financial_category(category_id: int):
    # TODO: Implement logic for Landlord to delete their custom category.
    # Landlord only, ensures category belongs to them and is_system_default is False.
    # Check if category is in use by any FinancialTransaction; if so, prevent deletion or require re-categorization.
    pass

# --- Financial Transaction Management (Landlord) ---
# POST /financial-transactions (Landlord records an income or expense)
def record_financial_transaction():
    # TODO: Implement logic for Landlord to record an income or expense.
    # Landlord only.
    # Request: { type ('INCOME'/'EXPENSE'), category_id (FK to UserFinancialCategory), description, amount, transaction_date,
    #            property_id (optional), lease_id (optional), maintenance_request_id (optional),
    #            document_id (optional, for receipt/invoice), vendor_name (optional), sub_category (optional),
    #            is_recurring (boolean, default:false), recurrence_frequency (optional enum),
    #            recurrence_end_date (optional date), next_due_date (optional, if master recurring record),
    #            parent_recurring_transaction_id (optional FK), is_tax_deductible_candidate (boolean), notes (optional) }
    # Creates a FinancialTransaction record. If is_recurring and no parent_id, this is a master recurring transaction.
    # If parent_id is present, this is an instance of a recurring transaction.
    # System might auto-generate instances from master records based on next_due_date and frequency.
    # Response: Full details of the created transaction.
    pass

# GET /financial-transactions (List transactions for landlord)
def list_financial_transactions():
    # TODO: Implement logic to list financial transactions for the authenticated Landlord.
    # Supports filtering by: property_id, lease_id, type, category_id, date_range, is_recurring, is_tax_deductible_candidate.
    # Supports pagination.
    pass

# GET /financial-transactions/{transaction_id} (Get specific transaction)
def get_financial_transaction_details(transaction_id: int):
    # TODO: Implement logic to get details of a specific financial transaction.
    # Landlord only.
    pass

# PUT /financial-transactions/{transaction_id} (Update transaction)
def update_financial_transaction(transaction_id: int):
    # TODO: Implement logic to update an existing financial transaction.
    # Landlord only. Request body contains fields to update (similar to create).
    # If updating a master recurring transaction, may need logic to update/warn about future instances.
    pass

# DELETE /financial-transactions/{transaction_id} (Delete transaction)
def delete_financial_transaction(transaction_id: int):
    # TODO: Implement logic to delete a financial transaction.
    # Landlord only.
    # If deleting a master recurring transaction, decide on handling future instances (delete or orphan).
    pass

# POST /financial-transactions/{transaction_id}/link-document (Link an uploaded document/receipt)
# (This functionality might be part of PUT /financial-transactions or handled by Document service linking back)
# def link_document_to_transaction(transaction_id: int):
#    # Request: { document_id }
#    # Updates FinancialTransaction.document_id.
#    pass

# Example (conceptual):
# @financial_tx_bp.route('/categories', methods=['POST'])
# def create_category_route(): # ...
#     return jsonify({"message": "Category created", "category_id": 1}), 201
#
# @financial_tx_bp.route('', methods=['POST'])
# def record_tx_route(): # ...
#     return jsonify({"message": "Transaction recorded", "transaction_id": 1}), 201
