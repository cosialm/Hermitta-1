# Placeholder for Payment (Manual Rent Tracking) API Endpoints (Refined for Phase 1 MVP)
# Actual implementation would use a web framework like Flask or FastAPI

# POST /payments (Landlord records a payment made for a lease)
def record_manual_payment():
    # TODO: Implement logic for a landlord to manually record a payment.
    # Landlord only (recorded_by_landlord_id from authenticated user).
    # Request body should include:
    #   - lease_id
    #   - payment_date (date the payment was made by tenant)
    #   - amount_paid
    #   - payment_method (from ManualPaymentMethod enum, e.g., "CASH_TO_LANDLORD", "MPESA_TO_LANDLORD_MANUAL")
    #   - reference_number (Optional: e.g., bank slip ID, M-Pesa transaction code provided by tenant)
    #   - notes (Optional)
    # Creates a Payment record.
    # Response: Full details of the recorded payment.
    pass

# GET /payments/{payment_id} (Get specific manually recorded payment details)
def get_manual_payment_details(payment_id: int):
    # TODO: Implement logic to get details of a specific manually recorded payment.
    # Accessible by Landlord who recorded it or is associated with the lease.
    # Response: Full payment details.
    pass

# GET /leases/{lease_id}/payments (List payments recorded for a specific lease)
def list_payments_for_lease(lease_id: int):
    # TODO: Implement logic to list payments recorded for a specific lease.
    # Accessible by Landlord of the property or Tenant linked to the lease (if tenant has access).
    # Response: List of payment details.
    pass

# GET /properties/{property_id}/payments (List all payments recorded for a property)
def list_payments_for_property(property_id: int):
    # TODO: Implement logic to list all payments recorded for various leases under a specific property.
    # Landlord only.
    # Response: List of payment details, possibly grouped by lease.
    pass

# Example (conceptual):
# from flask import Blueprint, request, jsonify
# # from ..models.payment import Payment, ManualPaymentMethod
#
# payment_bp = Blueprint('payments', __name__, url_prefix='/payments')
#
# @payment_bp.route('', methods=['POST'])
# def record_payment_route():
#     # data = request.get_json()
#     # landlord_id = get_current_user_id()
#     # Create Payment object with lease_id, payment_date, amount_paid, payment_method, reference_number, etc.
#     # payment.recorded_by_landlord_id = landlord_id
#     # payment.save()
#     return jsonify({"message": "Payment recorded successfully", "payment_id": 1, "details": "{...}"}), 201
#
# @payment_bp.route('/<int:payment_id>', methods=['GET'])
# def get_payment_route(payment_id):
#     # payment = Payment.query.get_or_404(payment_id)
#     # Check permissions (landlord owns lease/property)
#     return jsonify({"payment_id": payment.id, "amount_paid": payment.amount_paid}), 200
#
# @payment_bp.route('/lease/<int:lease_id>', methods=['GET']) # Example alternative route structure
# def list_lease_payments_route(lease_id):
#     # payments = Payment.query.filter_by(lease_id=lease_id).all()
#     # Check permissions
#     return jsonify([{"id": p.id, "amount_paid": p.amount_paid} for p in []]), 200 # Placeholder
#
# # Consider if /properties/{property_id}/payments is needed for MVP or if lease-based is enough.
# # It's a good reporting endpoint for landlords.
# @payment_bp.route('/property/<int:property_id>', methods=['GET']) # Example alternative route structure
# def list_property_payments_route(property_id):
#     # Fetch leases for property, then payments for those leases.
#     # Check permissions
#     return jsonify([]), 200 # Placeholder
