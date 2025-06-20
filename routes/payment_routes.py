# Placeholder for Payment API Endpoints (Phase 2: Online Payments & Communication)
# Actual implementation would use a web framework like Flask or FastAPI

# --- Manual Payment Recording (from Phase 1, refined) ---
# POST /payments/manual (Landlord records a manual payment)
def record_manual_payment():
    # TODO: Implement logic for a landlord to manually record a payment.
    # Landlord only (recorded_by_landlord_id from authenticated user).
    # Request: {
    #            lease_id, payment_date, amount_paid,
    #            payment_method (e.g. "CASH_TO_LANDLORD", "MPESA_TO_LANDLORD_MANUAL", "BANK_DEPOSIT_LANDLORD"),
    #            reference_number (optional), notes (optional),
    #            // Fields specific to BANK_DEPOSIT_LANDLORD
    #            landlord_bank_account_id (optional, FK to LandlordBankAccount),
    #            bank_transaction_id (optional, from bank slip/statement),
    #            payer_narration (optional, from payer's bank transfer details)
    #          }
    # Creates/Updates a Payment record with status COMPLETED.
    # Response: Full details of the recorded payment, including bank_transaction_id, payer_narration, landlord_bank_account_id, and payment_reference_code if applicable.
    pass

# --- M-Pesa Online Payment Integration (New for Phase 2) ---
# POST /leases/{lease_id}/initiate-mpesa-payment (Tenant initiates STK push for a lease)
def initiate_mpesa_payment_for_lease(lease_id: int):
    # TODO: Implement logic for an authenticated tenant to initiate M-Pesa STK push.
    # Tenant only, for their active lease.
    # 1. Checks if landlord has active M-Pesa configuration (LandlordMpesaConfiguration).
    # 2. Creates/retrieves an 'EXPECTED' or 'PENDING_CONFIRMATION' Payment record for the lease's current due amount.
    #    (Payment.expected_amount, Payment.due_date are key).
    # 3. Generates a unique merchant_request_id.
    # 4. Creates an MpesaPaymentLog entry with PENDING_STK_PUSH status, linking to the Payment record ID if applicable.
    # 5. Calls M-Pesa STK Push API with landlord's credentials, amount, tenant's phone, callback URL, merchant_request_id.
    # 6. Updates MpesaPaymentLog with checkout_request_id and status (STK_PUSH_SUCCESSFUL/FAILED) from M-Pesa response.
    # 7. If STK push initiated successfully, updates Payment status to PENDING_CONFIRMATION and links MpesaPaymentLog.log_id.
    # Request: { amount (optional, defaults to amount_due on lease), phone_number (optional, defaults to user's phone for STK) }
    # Response: { success, message, merchant_request_id, checkout_request_id (if successful) }
    pass

# POST /mpesa/callback (External M-Pesa callback endpoint - platform-wide or landlord-specific if supported)
def mpesa_stk_callback():
    # TODO: Implement logic to handle M-Pesa STK push callback.
    # This is an external, unauthenticated endpoint hit by M-Pesa.
    # IMPORTANT: Validate the source/authenticity of the callback if possible (e.g., IP whitelisting, request signature if provided by M-Pesa).
    # 1. Parses the M-Pesa JSON payload from the callback.
    # 2. Finds the corresponding MpesaPaymentLog record using checkout_request_id from the payload.
    # 3. Updates MpesaPaymentLog with callback_payload, mpesa_receipt_number, amount_paid, transaction_date,
    #    and status (PAYMENT_CONFIRMED_CALLBACK or PAYMENT_FAILED_CALLBACK).
    # 4. If payment successful (ResultCode is 0 in callback):
    #    a. Finds/Updates the associated Payment record: status to COMPLETED, amount_paid, payment_date, payment_method to MPESA_ONLINE_STK.
    #    b. Triggers notification (using Notification model) to tenant and landlord.
    #    c. (Future) Potentially updates lease balance or generates a financial transaction.
    # 5. If payment failed (non-zero ResultCode or other error indicators):
    #    a. Updates Payment record status to FAILED.
    #    b. Triggers notification to tenant (and possibly landlord).
    # Response: Acknowledgement to M-Pesa (e.g., {"ResultCode": 0, "ResultDesc": "Accepted"}).
    pass

# --- General Payment Viewing ---
# GET /payments (List payments - with filters)
def list_payments():
    # TODO: Implement logic to list payments.
    # For Landlord: All payments related to their leases/properties (Payment records).
    # For Tenant: Payments they made or are expected for their leases.
    # Query Params: lease_id, property_id, status (e.g., "COMPLETED", "PENDING_CONFIRMATION", "EXPECTED"),
    #               payment_method, date_range (for due_date or payment_date).
    # Response: List of Payment records, each including bank_transaction_id, payer_narration, landlord_bank_account_id, and payment_reference_code if applicable.
    pass

# GET /payments/{payment_id} (Get specific payment details)
def get_payment_details(payment_id: int):
    # TODO: Implement logic to get details of a specific payment.
    # Accessible by Landlord or Tenant involved in the payment.
    # Response: Full Payment details, including bank_transaction_id, payer_narration, landlord_bank_account_id, payment_reference_code if applicable, and may include linked MpesaPaymentLog info.
    pass

# GET /mpesa-transactions (Landlord views their M-Pesa transaction logs)
def list_landlord_mpesa_transactions():
    # TODO: Implement logic for Landlord to view their MpesaPaymentLog entries.
    # Landlord only (landlord_id from MpesaPaymentLog via Lease -> Property -> Landlord, or direct if added).
    # Query Params: lease_id, status (MpesaLogStatus), date_range, mpesa_receipt_number.
    # Response: List of MpesaPaymentLog records.
    pass

# Placeholder (New function)
# GET /tenant/payments/{payment_id}/obligation (Tenant views how to pay a specific bill)
def get_tenant_payment_obligation_details(payment_id: int):
    # TODO: Implement logic for a tenant to view payment instructions.
    # Tenant only, for their own payment obligations.
    # 1. Fetch the Payment record using payment_id. Ensure it belongs to the authenticated tenant.
    # 2. If payment_method is not yet set, or if it's something like BANK_DEPOSIT_LANDLORD:
    #    a. Fetch associated Landlord's bank accounts (e.g., LandlordBankAccount.query.filter_by(landlord_id=payment.lease.property.landlord_id, is_primary=True).first()).
    #    b. If a landlord bank account is found:
    #       - payment_details_to_display = {
    #           "payment_id": payment.id,
    #           "expected_amount": payment.expected_amount,
    #           "due_date": payment.due_date,
    #           "payment_reference_code": payment.payment_reference_code, # Crucial for reconciliation
    #           "bank_account_details": {
    #               "bank_name": landlord_bank_account.bank_name,
    #               "account_holder_name": landlord_bank_account.account_holder_name,
    #               "account_number": landlord_bank_account.account_number,
    #               "branch_name": landlord_bank_account.branch_name
    #           },
    #           "instructions": f"Please use the reference code '{payment.payment_reference_code}' in your bank transfer narration."
    #       }
    #    c. If no bank account is configured by landlord, provide a generic message.
    # 3. Return these details to the tenant.
    # Response: { payment_obligation_details }
    pass

# --- Generic Payment Initiation (New for Multi-Gateway Support) ---
# POST /payments/initiate-payment (User initiates a payment for an item)
def initiate_general_payment():
    # TODO: Implement logic for initiating a payment through various gateways.
    # This is intended to be a more generic version of initiate_mpesa_payment_for_lease.
    # Request: {
    #   item_id: str, (e.g., lease_id, invoice_id for which payment is made)
    #   item_type: str, (e.g., "LEASE_RENT", "INVOICE")
    #   amount: Decimal, (Optional: if not predefined by the item_id)
    #   currency: str, (e.g., "KES")
    #   payment_gateway_choice: str (e.g., "MPESA_DIRECT", "PESAPAL", "CARD_PESAPAL")
    #   phone_number: Optional[str] (for STK push via M-Pesa Direct or Pesapal M-Pesa)
    #   customer_email: Optional[str] (for card payments, receipts)
    #   customer_name: Optional[str]
    # }
    #
    # Logic:
    # 1. Validate request, retrieve item to be paid (e.g. Lease, Invoice), confirm amount.
    # 2. Identify landlord_id associated with the item.
    # 3. Create a main `Payment` record in `PENDING` or `EXPECTED` status.
    # 4. Based on `payment_gateway_choice`:
    #    a. If "MPESA_DIRECT":
    #       - Fetch `LandlordMpesaConfiguration`.
    #       - Create `GatewayTransaction` (type MPESA_DIRECT).
    #       - Call M-Pesa STK Push API.
    #       - Update `GatewayTransaction` with M-Pesa refs (MerchantRequestID, CheckoutRequestID).
    #       - Response: { message: "STK push initiated", internal_payment_id: "...", gateway_transaction_id: "..." }
    #    b. If "PESAPAL" (or "CARD_PESAPAL", "MPESA_VIA_PESAPAL"):
    #       - Fetch `LandlordGatewayConfig` for Pesapal for the landlord.
    #       - Create `GatewayTransaction` (type PESAPAL, status PENDING).
    #       - Generate internal merchant_reference for Pesapal.
    #       - Call Pesapal's "SubmitOrder" API (v2 or v3) with amount, currency, merchant_reference, description,
    #         callback_url (pointing to /webhooks/payment/pesapal), notification_id (for IPN), redirect_url, customer details.
    #       - Pesapal API returns a `redirect_url` and `pesapal_transaction_tracking_id`.
    #       - Update `GatewayTransaction` with `gateway_transaction_ref = pesapal_transaction_tracking_id`.
    #       - Response: { redirect_url: "pesapal_payment_page_url", internal_payment_id: "...", gateway_transaction_id: "..." }
    #    c. Other gateways (Stripe, Flutterwave) would follow similar patterns.
    #    d. If payment_gateway_choice is "BANK_TRANSFER" (or similar enum):
    #       - Generate and store `payment_reference_code` on the `Payment` record.
    #       - Fetch landlord's primary `LandlordBankAccount`.
    #       - Response: { message: "Bank transfer details provided",
    #                     internal_payment_id: "...",
    #                     payment_reference_code: "...",
    #                     bank_details: { ... } }
    # 5. Ensure `GatewayTransaction` is linked to the main `Payment` record.
    # 6. The `initiate_mpesa_payment_for_lease` might be refactored to use this generic flow or be deprecated.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.payment import Payment, PaymentMethod, PaymentStatus
# # from ..models.mpesa_payment_log import MpesaPaymentLog
#
# payment_bp = Blueprint('payments', __name__, url_prefix='/payments')
# mpesa_callbacks_bp = Blueprint('mpesa_callbacks', __name__, url_prefix='/callbacks/mpesa') # Different prefix for callbacks
#
# @payment_bp.route('/manual', methods=['POST'])
# def record_manual_payment_route(): # ...
#     return jsonify({"message": "Manual payment recorded"}), 201
#
# @payment_bp.route('/leases/<int:lease_id>/initiate-mpesa', methods=['POST'])
# def initiate_mpesa_route(lease_id): # ...
#     return jsonify({"message": "M-Pesa STK push initiated"}), 200
#
# @mpesa_callbacks_bp.route('/stk', methods=['POST']) # e.g. /callbacks/mpesa/stk
# def stk_callback_route(): # ...
#     # data = request.get_json()
#     # Process M-Pesa callback data, update MpesaPaymentLog and Payment records
#     return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}), 200
#
# # ... other payment listing/details routes ...
