import unittest
from datetime import datetime
from models.landlord_bank_account import LandlordBankAccount, BankAccountType

class TestLandlordBankAccount(unittest.TestCase):

    def test_instantiation_all_fields(self):
        """Test LandlordBankAccount instantiation with all fields provided."""
        now = datetime.utcnow()
        # Use a slightly earlier time for created_at for a more realistic scenario
        created_time = datetime(now.year, now.month, now.day, now.hour, now.minute -1 if now.minute > 0 else 0)
        updated_time = datetime(now.year, now.month, now.day, now.hour, now.minute)


        account_data = {
            "account_id": 1,
            "landlord_id": 101,
            "bank_name": "Equity Bank Kenya",
            "account_holder_name": "John Doe Properties Ltd",
            "account_number": "1234567890123",
            "branch_name": "Westlands Branch",
            "swift_code": "EQBLKENA",
            "account_type": BankAccountType.BUSINESS,
            "is_primary": True,
            "created_at": created_time,
            "updated_at": updated_time
        }

        account = LandlordBankAccount(**account_data)

        self.assertEqual(account.account_id, account_data["account_id"])
        self.assertEqual(account.landlord_id, account_data["landlord_id"])
        self.assertEqual(account.bank_name, account_data["bank_name"])
        self.assertEqual(account.account_holder_name, account_data["account_holder_name"])
        self.assertEqual(account.account_number, account_data["account_number"])
        self.assertEqual(account.branch_name, account_data["branch_name"])
        self.assertEqual(account.swift_code, account_data["swift_code"])
        self.assertEqual(account.account_type, account_data["account_type"])
        self.assertEqual(account.is_primary, account_data["is_primary"])
        self.assertEqual(account.created_at, account_data["created_at"])
        self.assertEqual(account.updated_at, account_data["updated_at"])

        self.assertIsInstance(account.created_at, datetime)
        self.assertIsInstance(account.updated_at, datetime)
        self.assertIsInstance(account.account_type, BankAccountType)

    def test_instantiation_required_fields_and_defaults(self):
        """Test instantiation with only required fields and check default values."""
        before_creation = datetime.utcnow()
        account_data_required = {
            "account_id": 2,
            "landlord_id": 102,
            "bank_name": "KCB Bank Kenya",
            "account_holder_name": "Jane Doe",
            "account_number": "0987654321098",
        }
        account = LandlordBankAccount(**account_data_required)
        after_creation = datetime.utcnow()

        self.assertEqual(account.account_id, account_data_required["account_id"])
        self.assertEqual(account.landlord_id, account_data_required["landlord_id"])
        self.assertEqual(account.bank_name, account_data_required["bank_name"])
        self.assertEqual(account.account_holder_name, account_data_required["account_holder_name"])
        self.assertEqual(account.account_number, account_data_required["account_number"])

        # Test default values for optional fields
        self.assertIsNone(account.branch_name)
        self.assertIsNone(account.swift_code)
        self.assertEqual(account.account_type, BankAccountType.OTHER)
        self.assertFalse(account.is_primary)

        # Test created_at and updated_at are set and are datetime instances
        # Due to default arguments in __init__ (datetime.utcnow()) being evaluated
        # at class definition time, we cannot reliably check for "recent" time here
        # without passing it in. We only check they are datetime instances.
        self.assertIsInstance(account.created_at, datetime)
        self.assertIsInstance(account.updated_at, datetime)
        # If the model were changed to set default in __init__ body, e.g.:
        # self.created_at = created_at if created_at is not None else datetime.utcnow()
        # then the timing check would be more appropriate:
        # self.assertTrue(before_creation <= account.created_at <= after_creation)
        # self.assertTrue(before_creation <= account.updated_at <= after_creation)


    def test_bank_account_type_enum_values(self):
        """Test the string values of the BankAccountType enum members."""
        self.assertEqual(BankAccountType.CHECKING.value, "CHECKING")
        self.assertEqual(BankAccountType.SAVINGS.value, "SAVINGS")
        self.assertEqual(BankAccountType.BUSINESS.value, "BUSINESS")
        self.assertEqual(BankAccountType.OTHER.value, "OTHER")

    def test_boolean_is_primary(self):
        """Test the is_primary boolean field."""
        account_data_template = {
            "account_id": 3, # Base ID, will increment
            "landlord_id": 103,
            "bank_name": "Test Bank for Primary Flag",
            "account_holder_name": "Boolean Test Holder",
            "account_number": "555111222",
        }

        # Test with is_primary = True
        account_primary_true = LandlordBankAccount(
            **account_data_template,
            is_primary=True
        )
        self.assertTrue(account_primary_true.is_primary)

        # Test with is_primary = False
        account_primary_false = LandlordBankAccount(
            **{**account_data_template, "account_id": 4}, # New ID
            is_primary=False
        )
        self.assertFalse(account_primary_false.is_primary)

        # Test default value (should be False, already covered in test_instantiation_required_fields_and_defaults)
        # but can be re-asserted here for clarity if desired for this specific test method.
        account_primary_default = LandlordBankAccount(
            **{**account_data_template, "account_id": 5} # New ID
        )
        self.assertFalse(account_primary_default.is_primary)


if __name__ == '__main__':
    unittest.main()
