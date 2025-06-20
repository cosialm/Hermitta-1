from enum import Enum
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

# Phase 2: Combined Payment Methods and Statuses
class PaymentMethod(Enum):
    # Manual methods from Phase 1
    CASH_TO_LANDLORD = "CASH_TO_LANDLORD"
    BANK_DEPOSIT_LANDLORD = "BANK_DEPOSIT_LANDLORD"
    MPESA_TO_LANDLORD_MANUAL = "MPESA_TO_LANDLORD_MANUAL" # Manually recorded by landlord
    OTHER_MANUAL = "OTHER_MANUAL"

    # Online methods for Phase 2
    MPESA_ONLINE_STK = "MPESA_ONLINE_STK" # Tenant initiated via STK Push

class PaymentStatus(Enum):
    EXPECTED = "EXPECTED"               # Rent is due, payment record created automatically or by landlord as expectation
    PENDING_CONFIRMATION = "PENDING_CONFIRMATION" # Online payment initiated, awaiting callback
    COMPLETED = "COMPLETED"             # Payment confirmed (manual or online)
    PARTIALLY_PAID = "PARTIALLY_PAID"   # If partial payments are allowed and tracked
    FAILED = "FAILED"                   # Online payment failed, or manual entry was erroneous and voided
    OVERDUE = "OVERDUE"                 # Payment was expected but not completed by due date + grace period
    CANCELLED = "CANCELLED"             # E.g. STK push cancelled by user

class Payment:
    def __init__(self,
                 payment_id: int,
                 lease_id: int, # Foreign Key to Lease
                 expected_amount: Decimal, # Amount expected (e.g. monthly rent)
                 due_date: Optional[date] = None, # When this payment is due
                 payment_method: Optional[PaymentMethod] = None, # Can be None if just an 'EXPECTED' record
                 amount_paid: Optional[Decimal] = None, # Actual amount paid, filled upon completion
                 payment_date: Optional[date] = None, # Actual date payment was made/confirmed
                 status: PaymentStatus = PaymentStatus.EXPECTED,
                 recorded_by_landlord_id: Optional[int] = None, # FK to User (Landlord who records manual payment)
                 initiated_by_user_id: Optional[int] = None, # FK to User (Tenant who initiates online payment)
                 online_transaction_log_id: Optional[int] = None, # FK to MpesaPaymentLog or similar
                 reference_number: Optional[str] = None, # For manual methods or external ref
                 notes: Optional[str] = None,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.payment_id = payment_id
        self.lease_id = lease_id
        self.expected_amount = expected_amount
        self.due_date = due_date

        self.payment_method = payment_method
        self.amount_paid = amount_paid
        self.payment_date = payment_date
        self.status = status

        self.recorded_by_landlord_id = recorded_by_landlord_id
        self.initiated_by_user_id = initiated_by_user_id
        self.online_transaction_log_id = online_transaction_log_id # e.g., MpesaPaymentLog.log_id

        self.reference_number = reference_number
        self.notes = notes

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage (Phase 2):
# 1. Rent expected (auto-generated or by landlord)
# rent_due = Payment(payment_id=1, lease_id=101, expected_amount=Decimal("30000.00"),
#                    due_date=date(2024,8,1), status=PaymentStatus.EXPECTED)

# 2. Tenant initiates M-Pesa payment (this record might be created/updated after STK push)
# mpesa_intent = Payment(payment_id=2, lease_id=101, expected_amount=Decimal("30000.00"),
#                        due_date=date(2024,8,1), payment_method=PaymentMethod.MPESA_ONLINE_STK,
#                        initiated_by_user_id=201, # tenant_id
#                        status=PaymentStatus.PENDING_CONFIRMATION)
# # online_transaction_log_id would link to the MpesaPaymentLog entry for this attempt

# 3. Landlord records a manual cash payment
# manual_cash = Payment(payment_id=3, lease_id=102, expected_amount=Decimal("15000.00"),
#                       due_date=date(2024,8,5), payment_method=PaymentMethod.CASH_TO_LANDLORD,
#                       amount_paid=Decimal("15000.00"), payment_date=date(2024,8,3),
#                       recorded_by_landlord_id=1, status=PaymentStatus.COMPLETED,
#                       notes="Cash received for August rent.")
# print(rent_due.status)
# print(mpesa_intent.payment_method if mpesa_intent else "")
# print(manual_cash.amount_paid)
