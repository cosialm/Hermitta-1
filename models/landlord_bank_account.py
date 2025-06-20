from datetime import datetime
from typing import Optional
from enum import Enum

class BankAccountType(Enum):
    CHECKING = "CHECKING"
    SAVINGS = "SAVINGS"
    BUSINESS = "BUSINESS"
    OTHER = "OTHER"

class LandlordBankAccount:
    def __init__(self,
                 account_id: int, # PK
                 landlord_id: int, # FK to User model
                 bank_name: str,
                 account_holder_name: str,
                 account_number: str, # Consider security implications if this needs to be encrypted
                 branch_name: Optional[str] = None,
                 swift_code: Optional[str] = None,
                 account_type: Optional[BankAccountType] = BankAccountType.OTHER,
                 is_primary: bool = False, # Landlord can mark one account as primary
                 created_at: datetime = datetime.utcnow(),
                 updated_at: datetime = datetime.utcnow()):

        self.account_id = account_id
        self.landlord_id = landlord_id
        self.bank_name = bank_name
        self.account_holder_name = account_holder_name
        self.account_number = account_number
        self.branch_name = branch_name
        self.swift_code = swift_code
        self.account_type = account_type
        self.is_primary = is_primary
        self.created_at = created_at
        self.updated_at = updated_at

# Example Usage:
# primary_account = LandlordBankAccount(
#     account_id=1,
#     landlord_id=10, # Assuming landlord user_id 10
#     bank_name="Equity Bank Kenya",
#     account_holder_name="John Doe Properties Ltd",
#     account_number="1234567890123",
#     branch_name="Westlands Branch",
#     swift_code="EQBLKENA",
#     account_type=BankAccountType.BUSINESS,
#     is_primary=True
# )
#
# secondary_account = LandlordBankAccount(
#     account_id=2,
#     landlord_id=10,
#     bank_name="KCB Bank Kenya",
#     account_holder_name="John Doe",
#     account_number="0987654321098",
#     branch_name="Sarit Centre Branch",
#     swift_code="KCBLKENX",
#     account_type=BankAccountType.CHECKING,
#     is_primary=False
# )
#
# print(f"Primary Account: {primary_account.bank_name} - {primary_account.account_number}")
# print(f"Secondary Account Holder: {secondary_account.account_holder_name}, Type: {secondary_account.account_type.value if secondary_account.account_type else 'N/A'}")
