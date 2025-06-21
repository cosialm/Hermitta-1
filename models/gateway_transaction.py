import enum
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal
from hermitta_app import db # Main SQLAlchemy db instance
from .enums import GatewayType, GatewayTransactionStatus # Import centralized enums

# from .payment import Payment # Will be linked via backref from Payment model

# Local Enums MOVED to models.enums.py:
# class GatewayTransactionStatus(enum.Enum):
#     PENDING = "PENDING"
#     # ... (rest of enum definition)
# class GatewayType(enum.Enum):
#     MPESA_STK_PUSH = "MPESA_STK_PUSH"
#     # ... (rest of enum definition)

class GatewayTransaction(db.Model):
    __tablename__ = 'gateway_transactions'

    transaction_id = db.Column(db.Integer, primary_key=True)
    # ForeignKey to payments.payment_id
    # A single Payment might have multiple GatewayTransaction attempts (e.g. initial attempt failed, user retried)
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'), nullable=False, index=True)

    gateway_type = db.Column(db.Enum(GatewayType), nullable=False)

    # Unique ID from the payment gateway (e.g., Pesapal tracking ID, M-Pesa transaction ID, Stripe charge ID)
    gateway_specific_transaction_id = db.Column(db.String(255), nullable=True, index=True)
    # Our internal unique reference sent to the gateway, if applicable (e.g. merchant transaction ID)
    internal_merchant_ref = db.Column(db.String(255), nullable=True, index=True)

    status = db.Column(db.Enum(GatewayTransactionStatus), default=GatewayTransactionStatus.PENDING, nullable=False, index=True)

    amount = db.Column(db.Numeric(12, 2), nullable=False) # Amount processed by the gateway
    currency = db.Column(db.String(10), nullable=False) # Currency code (e.g., "KES", "USD")

    # Specific payment method used at the gateway, if provided by gateway (e.g., "CARD", "MPESA", "AIRTELMONEY")
    payment_method_detail = db.Column(db.String(100), nullable=True)

    # Store payloads for debugging and auditing. Be careful about storing full sensitive data.
    # Consider encrypting sensitive parts if stored, or omitting them.
    raw_request_payload = db.Column(db.JSON, nullable=True) # What we sent to the gateway
    raw_response_payload = db.Column(db.JSON, nullable=True) # Initial synchronous response from gateway
    callback_payload = db.Column(db.JSON, nullable=True) # Full callback/webhook data from the gateway

    error_code = db.Column(db.String(100), nullable=True) # Gateway-specific error code
    error_message = db.Column(db.Text, nullable=True) # Gateway-specific error message

    notes = db.Column(db.Text, nullable=True) # Internal notes regarding this gateway transaction

    initiated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # When this gateway transaction was initiated
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False) # When this record was last updated

    # Relationship back to Payment
    # A payment can have multiple gateway transaction attempts.
    payment = db.relationship('Payment', backref=db.backref('gateway_transactions_attempts', lazy='dynamic'))

    def __repr__(self):
        return f"<GatewayTransaction {self.transaction_id} for Payment {self.payment_id} - Gateway: {self.gateway_type.value} Status: {self.status.value}>"

# Example:
# If a Payment of KES 5000 is initiated via Pesapal:
# 1. A Payment record is created (status e.g. PENDING_CONFIRMATION).
# 2. A GatewayTransaction record is created:
#    payment_id = (ID of the Payment record)
#    gateway_type = GatewayType.PESAPAL
#    internal_merchant_ref = "UNIQUE_OUR_SYSTEM_REF_FOR_THIS_ATTEMPT"
#    amount = 5000.00
#    currency = "KES"
#    status = GatewayTransactionStatus.PENDING
#
# If the Pesapal callback indicates success:
#    GatewayTransaction status -> SUCCESSFUL
#    gateway_specific_transaction_id = "PESAPAL_TRACKING_ID"
#    Payment status -> COMPLETED
#
# If it fails:
#    GatewayTransaction status -> FAILED
#    Payment status -> might revert to EXPECTED or FAILED depending on logic.
# User might retry, creating a new GatewayTransaction record for the same Payment ID.
