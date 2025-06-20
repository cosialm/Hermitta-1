from enum import Enum
from datetime import datetime, date
from typing import Optional
from decimal import Decimal

class FinancialTransactionType(Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

# It's often good to have predefined categories, but allow for user-defined ones too.
# For an Enum approach, it would be:
class FinancialTransactionCategory(Enum):
    # Income Categories
    RENT = "RENT"
    LATE_FEE = "LATE_FEE"
    APPLICATION_FEE = "APPLICATION_FEE"
    OTHER_INCOME = "OTHER_INCOME" # Parking fees, laundry, etc.

    # Expense Categories
    REPAIRS_MAINTENANCE = "REPAIRS_MAINTENANCE"
    UTILITIES_PROPERTY = "UTILITIES_PROPERTY" # Paid by landlord
    PROPERTY_TAXES = "PROPERTY_TAXES"
    INSURANCE = "INSURANCE"
    MORTGAGE_PAYMENT = "MORTGAGE_PAYMENT" # Principal & Interest could be split
    MANAGEMENT_FEE = "MANAGEMENT_FEE"
    SUPPLIES = "SUPPLIES"
    LEGAL_FEES = "LEGAL_FEES"
    OTHER_EXPENSE = "OTHER_EXPENSE"
    # More categories as needed

class FinancialTransaction:
    def __init__(self,
                 transaction_id: int,
                 landlord_id: int, # Foreign Key to User
                 type: FinancialTransactionType,
                 category: str, # Can be from Enum or user-defined string
                 description: str,
                 amount: Decimal,
                 transaction_date: date,
                 property_id: Optional[int] = None, # FK to Property
                 lease_id: Optional[int] = None,    # FK to Lease
                 related_payment_id: Optional[int] = None, # FK to Payment
                 vendor_name: Optional[str] = None, # For expenses
                 receipt_url: Optional[str] = None, # URL to a scanned receipt (legacy, see Document model)
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.transaction_id = transaction_id
        self.property_id = property_id
        self.lease_id = lease_id
        self.landlord_id = landlord_id
        self.type = type
        self.category = category # Could use FinancialTransactionCategory(category).value if enforcing enum
        self.description = description
        self.amount = amount # Should always be positive; type (INCOME/EXPENSE) determines flow
        self.transaction_date = transaction_date
        self.related_payment_id = related_payment_id
        self.vendor_name = vendor_name
        self.receipt_url = receipt_url # Note: Will be superseded by linking to Document model
        self.created_at = created_at
        self.updated_at = updated_at

# Example usage:
# rent_income = FinancialTransaction(
#     transaction_id=1, landlord_id=1, type=FinancialTransactionType.INCOME,
#     category=FinancialTransactionCategory.RENT.value, # or "RENT" as string
#     description="Monthly rent for Apt 3B", amount=Decimal("1200.00"),
#     transaction_date=date(2024, 3, 1), lease_id=101, property_id=20
# )
#
# repair_expense = FinancialTransaction(
#     transaction_id=2, landlord_id=1, type=FinancialTransactionType.EXPENSE,
#     category=FinancialTransactionCategory.REPAIRS_MAINTENANCE.value,
#     description="Plumbing repair for leaky sink", amount=Decimal("150.00"),
#     transaction_date=date(2024, 3, 5), property_id=20, vendor_name="Quick Plumbers Inc."
# )
# print(rent_income.category, rent_income.amount)
# print(repair_expense.category, repair_expense.amount)
