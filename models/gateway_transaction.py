from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

# Assuming Payment model exists in models.payment (or similar)
# from .payment import Payment
# Assuming GatewayType from rental_management_mvp.models.landlord_gateway_config
# This creates a slight dependency; ideally, GatewayType might be defined more centrally if used widely.
# For now, let's assume it can be referenced or redefined if necessary.
class GatewayTransactionStatus(Enum):
    PENDING = "PENDING"         # Transaction initiated, awaiting confirmation
    SUCCESSFUL = "SUCCESSFUL"   # Payment confirmed by the gateway
    FAILED = "FAILED"           # Payment failed or was declined by the gateway
    CANCELLED = "CANCELLED"       # Payment was cancelled by user or system
    PROCESSING = "PROCESSING"     # Gateway is still processing (e.g., some bank transfers)
    REQUIRES_ACTION = "REQUIRES_ACTION" # e.g., 3DS authentication needed

class GatewayTypeEnum(Enum): # Redefining for local use if cross-module import is an issue in this context
    MPESA_DIRECT = "MPESA_DIRECT"
    PESAPAL = "PESAPAL"
    STRIPE = "STRIPE"
    FLUTTERWAVE = "FLUTTERWAVE"
    OTHER = "OTHER"

class GatewayTransaction:
    def __init__(self,
                 transaction_id: int, # PK
                 payment_id: int, # FK to our internal Payment model
                 gateway_type: GatewayTypeEnum,
                 gateway_transaction_ref: Optional[str] = None, # Unique ID from the gateway (e.g., Pesapal tracking ID)
                 gateway_merchant_ref: Optional[str] = None, # Our internal unique reference sent to the gateway
                 status: GatewayTransactionStatus = GatewayTransactionStatus.PENDING,
                 amount: Decimal, # Amount processed by the gateway
                 currency: str, # Currency code (e.g., "KES")
                 payment_method_used: Optional[str] = None, # e.g., "CARD", "MPESA", "AIRTELMONEY" (provided by gateway)
                 raw_request_payload: Optional[Dict[str, Any]] = None, # What we sent to the gateway (excluding sensitive details)
                 raw_response_payload: Optional[Dict[str, Any]] = None, # Initial response from gateway after submission
                 callback_payload: Optional[Dict[str, Any]] = None, # Full callback/webhook data from the gateway
                 error_code: Optional[str] = None, # Gateway-specific error code
                 error_message: Optional[str] = None, # Gateway-specific error message
                 notes: Optional[str] = None, # Internal notes
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.transaction_id = transaction_id
        self.payment_id = payment_id
        self.gateway_type = gateway_type
        self.gateway_transaction_ref = gateway_transaction_ref
        self.gateway_merchant_ref = gateway_merchant_ref
        self.status = status
        self.amount = amount
        self.currency = currency
        self.payment_method_used = payment_method_used
        self.raw_request_payload = raw_request_payload
        self.raw_response_payload = raw_response_payload
        self.callback_payload = callback_payload
        self.error_code = error_code
        self.error_message = error_message
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# pesapal_gtx = GatewayTransaction(
#     transaction_id=1001,
#     payment_id=201, # Internal Payment ID
#     gateway_type=GatewayTypeEnum.PESAPAL,
#     gateway_merchant_ref="OUR_UNIQUE_REF_123",
#     amount=Decimal("5000.00"),
#     currency="KES",
#     status=GatewayTransactionStatus.PENDING
# )
#
# # After successful callback:
# # pesapal_gtx.status = GatewayTransactionStatus.SUCCESSFUL
# # pesapal_gtx.gateway_transaction_ref = "PESAPAL_TRACK_ID_ABC"
# # pesapal_gtx.payment_method_used = "MPESA"
# # pesapal_gtx.callback_payload = {"data": "full_pesapal_callback_data"}
# # pesapal_gtx.updated_at = datetime.utcnow()
#
# print(pesapal_gtx.gateway_type, pesapal_gtx.gateway_merchant_ref, pesapal_gtx.status)
