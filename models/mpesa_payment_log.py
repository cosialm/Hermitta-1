from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

class MpesaLogStatus(Enum):
    PENDING_STK_PUSH = "PENDING_STK_PUSH"
    STK_PUSH_INITIATED = "STK_PUSH_INITIATED"
    STK_PUSH_SUCCESSFUL = "STK_PUSH_SUCCESSFUL"    # M-Pesa confirmed STK push was sent to user's phone (sync or async)
    STK_PUSH_FAILED = "STK_PUSH_FAILED"            # M-Pesa indicated STK push itself failed (e.g., invalid number, system error)
    PAYMENT_CONFIRMED_CALLBACK = "PAYMENT_CONFIRMED_CALLBACK" # Callback received, payment successful
    PAYMENT_FAILED_CALLBACK = "PAYMENT_FAILED_CALLBACK"       # Callback received, payment failed or cancelled by user on phone
    CALLBACK_PROCESSING_ERROR = "CALLBACK_PROCESSING_ERROR" # Callback received but error during our internal processing
    TIMEOUT_AWAITING_CALLBACK = "TIMEOUT_AWAITING_CALLBACK" # STK push was successful, but no callback received within expected time
    STK_PUSH_TIMEOUT_AWAITING_QUERY = "STK_PUSH_TIMEOUT_AWAITING_QUERY" # After TIMEOUT_AWAITING_CALLBACK, system should query M-Pesa for status
    QUERY_SUCCESS_PAYMENT_CONFIRMED = "QUERY_SUCCESS_PAYMENT_CONFIRMED" # Status Query API confirmed payment
    QUERY_SUCCESS_PAYMENT_FAILED = "QUERY_SUCCESS_PAYMENT_FAILED"       # Status Query API confirmed payment failed or not made
    QUERY_FAILED = "QUERY_FAILED"                                 # Status Query API call itself failed
    UNKNOWN = "UNKNOWN"                                         # Other states or errors

class MpesaPaymentLog:
    def __init__(self,
                 log_id: int,
                 lease_id: int,
                 tenant_id: int,
                 amount_requested: Decimal,
                 phone_number_stk_pushed_to: str,
                 merchant_request_id: str, # Our unique ID for the STK push request
                 checkout_request_id: Optional[str] = None, # M-Pesa's unique ID for the STK push transaction
                 payment_id: Optional[int] = None, # FK to Payment, if a Payment intent record exists
                 amount_paid: Optional[Decimal] = None,
                 mpesa_receipt_number: Optional[str] = None, # Indexed
                 transaction_date: Optional[datetime] = None, # Timestamp from M-Pesa callback or query
                 status: MpesaLogStatus = MpesaLogStatus.PENDING_STK_PUSH,
                 stk_push_response_payload: Optional[Dict[str, Any]] = None, # To store M-Pesa's immediate response to STK push
                 stk_failure_reason: Optional[str] = None, # If STK push fails immediately
                 callback_payload: Optional[Dict[str, Any]] = None, # To store the raw callback from M-Pesa
                 query_api_response_payload: Optional[Dict[str, Any]] = None, # To store response from M-Pesa Query API
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.log_id = log_id
        self.payment_id = payment_id
        self.lease_id = lease_id
        self.tenant_id = tenant_id
        self.amount_requested = amount_requested
        self.amount_paid = amount_paid

        self.phone_number_stk_pushed_to = phone_number_stk_pushed_to
        self.merchant_request_id = merchant_request_id
        self.checkout_request_id = checkout_request_id

        self.mpesa_receipt_number = mpesa_receipt_number
        self.transaction_date = transaction_date

        self.status = status
        self.stk_push_response_payload = stk_push_response_payload
        self.stk_failure_reason = stk_failure_reason
        self.callback_payload = callback_payload
        self.query_api_response_payload = query_api_response_payload # Store query response

        self.created_at = created_at
        self.updated_at = updated_at
