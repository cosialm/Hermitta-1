from enum import Enum
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

class VendorInvoiceStatus(Enum):
    DRAFT = "DRAFT"                 # Vendor is preparing the invoice
    SUBMITTED = "SUBMITTED"           # Vendor submitted to Landlord for payment
    VIEWED_BY_LANDLORD = "VIEWED_BY_LANDLORD"
    APPROVED_FOR_PAYMENT = "APPROVED_FOR_PAYMENT" # Landlord approved, pending payment processing
    PARTIALLY_PAID = "PARTIALLY_PAID" # Partial payment made
    PAID = "PAID"                     # Fully paid
    OVERDUE = "OVERDUE"               # Past due date and not fully paid
    CANCELLED = "CANCELLED"           # Invoice cancelled by vendor or landlord agreement
    IN_DISPUTE = "IN_DISPUTE"         # Landlord is disputing the invoice

class VendorInvoice:
    def __init__(self,
                 invoice_id: int,
                 maintenance_request_id: int, # Foreign Key to MaintenanceRequest
                 vendor_user_id: int, # Foreign Key to User (VENDOR role)
                 landlord_user_id: int, # Foreign Key to User (LANDLORD role - who needs to pay)
                 invoice_number: str, # Vendor's invoice number (should be unique per vendor)
                 amount_due: Decimal,
                 due_date: date,
                 quote_id: Optional[int] = None, # FK to Quote, if work was based on an approved quote
                 status: VendorInvoiceStatus = VendorInvoiceStatus.SUBMITTED,
                 payment_instructions: Optional[str] = None, # e.g., Bank details, M-Pesa Paybill/Till
                 submitted_at: Optional[datetime] = None, # When vendor submits
                 approved_at: Optional[datetime] = None, # When landlord approves for payment
                 paid_at: Optional[datetime] = None, # When fully paid
                 invoice_document_id: Optional[int] = None, # FK to Document model for uploaded PDF invoice
                 # Link to the FinancialTransaction record when landlord records this as an EXPENSE
                 linked_financial_transaction_id: Optional[int] = None,
                 notes_by_vendor: Optional[str] = None,
                 notes_by_landlord: Optional[str] = None, # e.g., "Payment processed via cheque #123"
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.invoice_id = invoice_id
        self.maintenance_request_id = maintenance_request_id
        self.vendor_user_id = vendor_user_id
        self.landlord_user_id = landlord_user_id

        self.invoice_number = invoice_number
        self.amount_due = amount_due
        self.due_date = due_date
        self.quote_id = quote_id # Link to the original quote if any
        self.status = status

        self.payment_instructions = payment_instructions
        self.submitted_at = submitted_at if submitted_at else (datetime.utcnow() if status == VendorInvoiceStatus.SUBMITTED else None)
        self.approved_at = approved_at
        self.paid_at = paid_at

        self.invoice_document_id = invoice_document_id # Link to an uploaded document
        self.linked_financial_transaction_id = linked_financial_transaction_id

        self.notes_by_vendor = notes_by_vendor
        self.notes_by_landlord = notes_by_landlord

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# plumbing_invoice = VendorInvoice(
#     invoice_id=1, maintenance_request_id=501, vendor_user_id=301, landlord_user_id=10,
#     invoice_number="INV-2024-005",
#     amount_due=Decimal("2500.00"),
#     due_date=date(2024, 4, 30),
#     quote_id=1, # Linked to the previously approved quote
#     status=VendorInvoiceStatus.SUBMITTED,
#     payment_instructions="Pay to KCB Bank, Acc No: 123456789, Acc Name: Joe's Plumbing",
#     submitted_at=datetime.utcnow()
# )
#
# # After landlord processes payment:
# # plumbing_invoice.status = VendorInvoiceStatus.PAID
# # plumbing_invoice.paid_at = datetime.utcnow()
# # plumbing_invoice.notes_by_landlord = "Paid via bank transfer ref BT7788."
# # plumbing_invoice.linked_financial_transaction_id = 5001 # ID of the expense transaction
#
# print(plumbing_invoice.invoice_number, plumbing_invoice.amount_due, plumbing_invoice.status)
