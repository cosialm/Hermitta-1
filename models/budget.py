from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from enum import Enum # Added import here

class BudgetPeriodType(Enum): # Could be used if budgets are strictly monthly, quarterly etc.
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"
    CUSTOM_RANGE = "CUSTOM_RANGE" # For budgets defined by specific start/end dates

class Budget:
    def __init__(self,
                 budget_id: int,
                 landlord_id: int, # Foreign Key to User (Landlord)
                 name: str, # e.g., "2024 Annual Budget", "Q1 Property A Repairs Budget"
                 period_start_date: date,
                 period_end_date: date,
                 # Optional: Link to a specific property if budget is property-specific
                 property_id: Optional[int] = None, # FK to Property
                 notes: Optional[str] = None,
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.budget_id = budget_id
        self.landlord_id = landlord_id
        self.name = name
        self.period_start_date = period_start_date
        self.period_end_date = period_end_date
        self.property_id = property_id # If null, applies to landlord's overall finances for the period
        self.notes = notes
        self.created_at = created_at
        self.updated_at = updated_at
        # Budget line items will be in a separate model: BudgetItem

class BudgetItem:
    def __init__(self,
                 budget_item_id: int,
                 budget_id: int, # Foreign Key to Budget
                 category_id: int, # Foreign Key to UserFinancialCategory (tracks if it's Income/Expense via category.type)
                 budgeted_amount: Decimal,
                 notes: Optional[str] = None):

        self.budget_item_id = budget_item_id
        self.budget_id = budget_id
        self.category_id = category_id # e.g., "Rent Income", "Repairs", "Management Fees"
        self.budgeted_amount = budgeted_amount # Can be positive for income, positive for expense (type defined by category)
        self.notes = notes

# Example Usage:
# annual_budget_2024 = Budget(
#     budget_id=1, landlord_id=10, name="2024 Full Year Financial Budget",
#     period_start_date=date(2024, 1, 1), period_end_date=date(2024, 12, 31)
# )
#
# # Line items for this budget:
# rent_income_budget = BudgetItem(
#     budget_item_id=1, budget_id=annual_budget_2024.budget_id,
#     category_id=1, # Assuming category_id 1 is "Rent Received" (Income type)
#     budgeted_amount=Decimal("1200000.00") # Total expected rent for the year
# )
#
# repairs_expense_budget = BudgetItem(
#     budget_item_id=2, budget_id=annual_budget_2024.budget_id,
#     category_id=15, # Assuming category_id 15 is "General Repairs" (Expense type)
#     budgeted_amount=Decimal("100000.00") # Total expected repair costs
# )
#
# property_A_maintenance_budget_Q1 = Budget(
#     budget_id=2, landlord_id=10, name="Property A - Q1 Maintenance Budget",
#     property_id=101, # Specific to Property A
#     period_start_date=date(2024,1,1), period_end_date=date(2024,3,31)
# )
#
# plumbing_budget_item_propA_Q1 = BudgetItem(
#     budget_item_id=3, budget_id=property_A_maintenance_budget_Q1.budget_id,
#     category_id=16, # Assuming Cat 16 = "Plumbing Repairs"
#     budgeted_amount=Decimal("20000.00")
# )
# print(annual_budget_2024.name)
# print(f"Budget Item '{repairs_expense_budget.category_id}' amount: {repairs_expense_budget.budgeted_amount}")

# Need to import Enum for BudgetPeriodType, though it's not used directly in constructor here
# from enum import Enum # Removed from here
