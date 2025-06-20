from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any # For JSON callback_payload
from decimal import Decimal

class MpesaLogStatus(Enum):
    PENDING_STK_PUSH = "PENDING_STK_PUSH"           # STK Push about to be initiated
    STK_PUSH_INITIATED = "STK_PUSH_INITIATED"       # STK Push request sent to M-Pesa (awaiting their async response)
    STK_PUSH_SUCCESSFUL = "STK_PUSH_SUCCESSFUL"     # M-Pesa confirmed STK was successfully pushed (sync or async response)
    STK_PUSH_FAILED = "STK_PUSH_FAILED"             # M-Pesa indicated STK push failed (e.g., invalid number)
    PAYMENT_CONFIRMED_CALLBACK = "PAYMENT_CONFIRMED_CALLBACK" # Callback received, payment successful
    PAYMENT_FAILED_CALLBACK = "PAYMENT_FAILED_CALLBACK"       # Callback received, payment failed or cancelled by user
    CALLBACK_PROCESSING_ERROR = "CALLBACK_PROCESSING_ERROR" # Callback received but error during our processing
    TIMEOUT_AWAITING_CALLBACK = "TIMEOUT_AWAITING_CALLBACK" # Did not receive callback in expected time
    UNKNOWN = "UNKNOWN"                             # Other states or errors

class MpesaPaymentLog:
    def __init__(self,
                 log_id: int,
                 lease_id: int, # Foreign Key to Lease
                 tenant_id: int, # Foreign Key to User (Tenant)
                 amount_requested: Decimal,
                 phone_number_stk_pushed_to: str, # Should be standardized (e.g., 254xxxxxxxxx)
                 merchant_request_id: str, # Our unique ID for the STK push request
                 checkout_request_id: Optional[str] = None, # M-Pesa's unique ID for the STK push transaction
                 payment_id: Optional[int] = None, # FK to Payment, if a Payment intent record exists
                 amount_paid: Optional[Decimal] = None,
                 mpesa_receipt_number: Optional[str] = None, # Indexed
                 transaction_date: Optional[datetime] = None, # Timestamp from M-Pesa callback
                 status: MpesaLogStatus = MpesaLogStatus.PENDING_STK_PUSH,
                 stk_push_response_payload: Optional[Dict[str, Any]] = None, # To store M-Pesa's immediate response to STK push
                 stk_failure_reason: Optional[str] = None, # If STK push fails immediately
                 callback_payload: Optional[Dict[str, Any]] = None, # To store the raw callback from M-Pesa
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.log_id = log_id
        self.payment_id = payment_id # Optional link to a Payment "intent" record
        self.lease_id = lease_id
        self.tenant_id = tenant_id
        self.amount_requested = amount_requested
        self.amount_paid = amount_paid # Usually same as requested, but good to confirm from callback

        self.phone_number_stk_pushed_to = phone_number_stk_pushed_to
        self.merchant_request_id = merchant_request_id # Our system's ID
        self.checkout_request_id = checkout_request_id # M-Pesa's ID for the STK transaction

        self.mpesa_receipt_number = mpesa_receipt_number # From successful callback
        self.transaction_date = transaction_date # From successful callback (actual payment time)

        self.status = status
        self.stk_push_response_payload = stk_push_response_payload # Store M-Pesa's direct response to our STK request
        self.stk_failure_reason = stk_failure_reason
        self.callback_payload = callback_payload # Store the full M-Pesa callback

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# log_entry = MpesaPaymentLog(
#     log_id=1, lease_id=101, tenant_id=201, amount_requested=Decimal("5000.00"),
#     phone_number_stk_pushed_to="254712345678",
#     merchant_request_id="MERCH_TXN_001"
#     # checkout_request_id will be filled after M-Pesa responds to STK push
# )
# print(log_entry.merchant_request_id, log_entry.status)
