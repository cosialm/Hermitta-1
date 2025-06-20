from enum import Enum
from datetime import datetime
from typing import Optional

class FinancialTransactionType(Enum): # Should be consistent with FinancialTransaction model
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class UserFinancialCategory:
    def __init__(self,
                 category_id: int,
                 landlord_id: Optional[int], # FK to User. Null if it's a system-default category.
                 name: str, # e.g., "Rent Income", "Water Bill", "Repairs - Plumbing"
                 type: FinancialTransactionType, # INCOME or EXPENSE
                 is_system_default: bool = False, # True for predefined system categories
                 description: Optional[str] = None, # Optional description for the category
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.category_id = category_id
        self.landlord_id = landlord_id # Link to landlord if it's a custom category
        self.name = name # Must be unique per landlord + type, or globally for system defaults
        self.type = type
        self.is_system_default = is_system_default
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# system_rent_category = UserFinancialCategory(
#     category_id=1, landlord_id=None, name="Rent Received",
#     type=FinancialTransactionType.INCOME, is_system_default=True
# )
#
# landlord_custom_repair_category = UserFinancialCategory(
#     category_id=101, landlord_id=10, name="Emergency Plumbing Repairs",
#     type=FinancialTransactionType.EXPENSE, is_system_default=False,
#     description="Urgent plumbing work outside of regular maintenance."
# )
#
# print(system_rent_category.name, system_rent_category.type)
# print(landlord_custom_repair_category.name, landlord_custom_repair_category.landlord_id)
