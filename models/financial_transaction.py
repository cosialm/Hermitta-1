from enum import Enum
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

class FinancialTransactionType(Enum): # Should be consistent with UserFinancialCategory
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class RecurrenceFrequency(Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"
    BI_ANNUALLY = "BI_ANNUALLY" # Every 6 months
    EVERY_TWO_MONTHS = "EVERY_TWO_MONTHS"
    # Add more as needed

class FinancialTransaction:
    def __init__(self,
                 transaction_id: int,
                 landlord_id: int, # Foreign Key to User
                 type: FinancialTransactionType, # Automatically set based on category_id.type if linked
                 category_id: int, # Foreign Key to UserFinancialCategory
                 description: str,
                 amount: Decimal,
                 transaction_date: date, # Date the transaction occurred or was recorded
                 property_id: Optional[int] = None, # FK to Property
                 lease_id: Optional[int] = None,    # FK to Lease
                 related_payment_id: Optional[int] = None, # FK to Payment (e.g. if this is logging a rent payment)
                 maintenance_request_id: Optional[int] = None, # FK to MaintenanceRequest (for expenses)
                 document_id: Optional[int] = None, # FK to Document (for receipt/invoice)
                 vendor_name: Optional[str] = None, # For expenses, if not linked to a Vendor User
                 sub_category: Optional[str] = None, # User-defined further categorization, e.g., "Plumbing" under "Repairs"

                 # Recurrence fields
                 is_recurring: bool = False,
                 recurrence_frequency: Optional[RecurrenceFrequency] = None,
                 recurrence_end_date: Optional[date] = None,
                 next_due_date: Optional[date] = None, # System managed: next date this recurring tx is expected
                 parent_recurring_transaction_id: Optional[int] = None, # FK to self, if this is an instance of a recurring tx template

                 is_tax_deductible_candidate: bool = False, # Landlord marks this for their own tracking
                 notes: Optional[str] = None, # General notes about the transaction

                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.transaction_id = transaction_id
        self.landlord_id = landlord_id
        self.type = type # This should ideally align with the type of the linked category_id
        self.category_id = category_id # FK to UserFinancialCategory
        self.description = description
        self.amount = amount # Always positive; 'type' determines if it's income or expense
        self.transaction_date = transaction_date

        self.property_id = property_id
        self.lease_id = lease_id
        self.related_payment_id = related_payment_id
        self.maintenance_request_id = maintenance_request_id
        self.document_id = document_id # Link to an uploaded receipt/invoice in Document model
        self.vendor_name = vendor_name
        self.sub_category = sub_category

        self.is_recurring = is_recurring
        self.recurrence_frequency = recurrence_frequency
        self.recurrence_end_date = recurrence_end_date
        self.next_due_date = next_due_date # For the master recurring transaction record
        self.parent_recurring_transaction_id = parent_recurring_transaction_id # Links instances to the master

        self.is_tax_deductible_candidate = is_tax_deductible_candidate
        self.notes = notes

        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# # Master recurring expense template (e.g., monthly internet bill for a property)
# master_internet_bill = FinancialTransaction(
#     transaction_id=100, landlord_id=10, type=FinancialTransactionType.EXPENSE, category_id=5, # Cat 5 = "Utilities"
#     description="Property XYZ Internet Bill (Safaricom Fiber)", amount=Decimal("5000.00"),
#     transaction_date=date(2024,1,10), # Start date of recurrence or first instance
#     property_id=101, is_recurring=True, recurrence_frequency=RecurrenceFrequency.MONTHLY,
#     next_due_date=date(2024,2,10) # System would update this
# )
#
# # An actual instance of the above recurring bill for February
# feb_internet_bill = FinancialTransaction(
#     transaction_id=101, landlord_id=10, type=FinancialTransactionType.EXPENSE, category_id=5,
#     description="Property XYZ Internet Bill (Safaricom Fiber) - Feb 2024", amount=Decimal("5000.00"),
#     transaction_date=date(2024,2,10), property_id=101,
#     parent_recurring_transaction_id=master_internet_bill.transaction_id,
#     document_id=201 # Link to the uploaded Safaricom bill PDF for Feb
# )
#
# # One-off repair expense
# plumbing_repair = FinancialTransaction(
#     transaction_id=102, landlord_id=10, type=FinancialTransactionType.EXPENSE, category_id=3, # Cat 3 = "Repairs"
#     description="Fix leaking kitchen tap - Unit A5", amount=Decimal("1500.00"),
#     transaction_date=date(2024,2,15), property_id=102, lease_id=50, maintenance_request_id=77,
#     vendor_name="Kamau Plumbers", is_tax_deductible_candidate=True
# )
#
# print(master_internet_bill.description, master_internet_bill.next_due_date)
# print(feb_internet_bill.parent_recurring_transaction_id)
