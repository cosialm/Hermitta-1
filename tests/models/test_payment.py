import unittest
from datetime import datetime, date
from decimal import Decimal
from rental_management_mvp.models.payment import Payment, PaymentMethod, PaymentStatus

class TestPaymentModel(unittest.TestCase):

    def test_instantiation_bank_transfer(self):
        """Test Payment instantiation for a completed bank transfer."""
        test_payment_date = date(2023, 10, 26)
        test_due_date = date(2023, 10, 1) # Example due date

        payment_data = {
            "payment_id": 1,
            "lease_id": 101,
            "expected_amount": Decimal("50000.00"),
            "payment_method": PaymentMethod.BANK_DEPOSIT_LANDLORD,
            "landlord_bank_account_id": 5,
            "bank_transaction_id": "BANKTX123ABC",
            "payer_narration": "Rent payment for Unit A1, Oct 2023",
            "payment_reference_code": "LEASE101-PAY202310",
            "amount_paid": Decimal("50000.00"),
            "payment_date": test_payment_date,
            "due_date": test_due_date,
            "status": PaymentStatus.COMPLETED,
            # For created_at/updated_at, we'll check type and existence due to default arg behavior
        }

        payment = Payment(**payment_data)

        self.assertEqual(payment.payment_id, payment_data["payment_id"])
        self.assertEqual(payment.lease_id, payment_data["lease_id"])
        self.assertEqual(payment.expected_amount, payment_data["expected_amount"])
        self.assertIsInstance(payment.expected_amount, Decimal)
        self.assertEqual(payment.payment_method, payment_data["payment_method"])
        self.assertEqual(payment.landlord_bank_account_id, payment_data["landlord_bank_account_id"])
        self.assertEqual(payment.bank_transaction_id, payment_data["bank_transaction_id"])
        self.assertEqual(payment.payer_narration, payment_data["payer_narration"])
        self.assertEqual(payment.payment_reference_code, payment_data["payment_reference_code"])
        self.assertEqual(payment.amount_paid, payment_data["amount_paid"])
        self.assertIsInstance(payment.amount_paid, Decimal)
        self.assertEqual(payment.payment_date, payment_data["payment_date"])
        self.assertIsInstance(payment.payment_date, date)
        self.assertEqual(payment.due_date, payment_data["due_date"])
        self.assertIsInstance(payment.due_date, date)
        self.assertEqual(payment.status, payment_data["status"])

        self.assertIsInstance(payment.created_at, datetime)
        self.assertIsInstance(payment.updated_at, datetime)

    def test_instantiation_manual_cash_completed(self):
        """Test Payment instantiation for a completed manually recorded cash payment."""
        test_due_date = date(2024, 1, 1)
        test_payment_date = date(2024, 1, 3)
        payment_data = {
            "payment_id": 4,
            "lease_id": 104,
            "expected_amount": Decimal("5000.00"),
            "due_date": test_due_date,
            "payment_method": PaymentMethod.CASH_TO_LANDLORD,
            "amount_paid": Decimal("5000.00"),
            "payment_date": test_payment_date,
            "recorded_by_landlord_id": 11, # Landlord's user ID
            "status": PaymentStatus.COMPLETED,
            "notes": "Cash received for Jan rent, Unit B2."
        }
        payment = Payment(**payment_data)

        self.assertEqual(payment.payment_id, payment_data["payment_id"])
        self.assertEqual(payment.lease_id, payment_data["lease_id"])
        self.assertEqual(payment.expected_amount, payment_data["expected_amount"])
        self.assertEqual(payment.due_date, payment_data["due_date"])
        self.assertEqual(payment.payment_method, payment_data["payment_method"])
        self.assertEqual(payment.amount_paid, payment_data["amount_paid"])
        self.assertEqual(payment.payment_date, payment_data["payment_date"])
        self.assertEqual(payment.recorded_by_landlord_id, payment_data["recorded_by_landlord_id"])
        self.assertEqual(payment.status, payment_data["status"])
        self.assertEqual(payment.notes, payment_data["notes"])

        # Check other relevant fields are None or default
        self.assertIsNone(payment.initiated_by_user_id)
        self.assertIsNone(payment.gateway_transaction_id)
        self.assertIsNone(payment.landlord_bank_account_id)
        self.assertIsNone(payment.bank_transaction_id)

        self.assertIsInstance(payment.created_at, datetime)
        self.assertIsInstance(payment.updated_at, datetime)

    def test_instantiation_mpesa_online_pending(self):
        """Test Payment instantiation for a pending M-Pesa online payment."""
        test_due_date = date(2023, 12, 1)
        payment_data = {
            "payment_id": 3,
            "lease_id": 103,
            "expected_amount": Decimal("10000.00"),
            "due_date": test_due_date,
            "payment_method": PaymentMethod.MPESA_ONLINE_STK,
            "initiated_by_user_id": 201, # Tenant's user ID
            "status": PaymentStatus.PENDING_CONFIRMATION,
        }
        payment = Payment(**payment_data)

        self.assertEqual(payment.payment_id, payment_data["payment_id"])
        self.assertEqual(payment.lease_id, payment_data["lease_id"])
        self.assertEqual(payment.expected_amount, payment_data["expected_amount"])
        self.assertEqual(payment.due_date, payment_data["due_date"])
        self.assertEqual(payment.payment_method, payment_data["payment_method"])
        self.assertEqual(payment.initiated_by_user_id, payment_data["initiated_by_user_id"])
        self.assertEqual(payment.status, payment_data["status"])

        # Check other relevant fields are None or default
        self.assertIsNone(payment.amount_paid)
        self.assertIsNone(payment.payment_date)
        self.assertIsNone(payment.recorded_by_landlord_id)
        self.assertIsNone(payment.gateway_transaction_id)
        self.assertIsNone(payment.landlord_bank_account_id)

        self.assertIsInstance(payment.created_at, datetime)
        self.assertIsInstance(payment.updated_at, datetime)


    def test_instantiation_expected_payment(self):
        """Test Payment instantiation for an 'expected' payment and check defaults."""
        test_due_date = date(2023, 11, 1)
        payment_data = {
            "payment_id": 2,
            "lease_id": 102,
            "expected_amount": Decimal("25000.00"),
            "due_date": test_due_date,
        }
        payment = Payment(**payment_data)

        self.assertEqual(payment.payment_id, payment_data["payment_id"])
        self.assertEqual(payment.lease_id, payment_data["lease_id"])
        self.assertEqual(payment.expected_amount, payment_data["expected_amount"])
        self.assertIsInstance(payment.expected_amount, Decimal)
        self.assertEqual(payment.due_date, test_due_date)
        self.assertIsInstance(payment.due_date, date)

        # Test default values
        self.assertEqual(payment.status, PaymentStatus.EXPECTED)
        self.assertIsNone(payment.payment_method)
        self.assertIsNone(payment.amount_paid)
        self.assertIsNone(payment.payment_date)
        self.assertIsNone(payment.recorded_by_landlord_id)
        self.assertIsNone(payment.initiated_by_user_id)
        self.assertIsNone(payment.gateway_transaction_id)
        self.assertIsNone(payment.reference_number)
        self.assertIsNone(payment.notes)
        self.assertIsNone(payment.landlord_bank_account_id)
        self.assertIsNone(payment.bank_transaction_id)
        self.assertIsNone(payment.payer_narration)
        self.assertIsNone(payment.payment_reference_code)

        self.assertIsInstance(payment.created_at, datetime)
        self.assertIsInstance(payment.updated_at, datetime)

    def test_enum_field_types(self):
        """Test that payment_method and status fields are instances of their Enums."""
        payment_data_enums = {
            "payment_id": 5,
            "lease_id": 105,
            "expected_amount": Decimal("100.00"),
            "payment_method": PaymentMethod.OTHER_MANUAL,
            "status": PaymentStatus.PARTIALLY_PAID,
        }
        payment = Payment(**payment_data_enums)

        self.assertIsInstance(payment.payment_method, PaymentMethod)
        self.assertEqual(payment.payment_method, PaymentMethod.OTHER_MANUAL)
        self.assertIsInstance(payment.status, PaymentStatus)
        self.assertEqual(payment.status, PaymentStatus.PARTIALLY_PAID)

        # Test with default status
        payment_data_default_status = {
            "payment_id": 6,
            "lease_id": 106,
            "expected_amount": Decimal("200.00"),
        }
        payment_default = Payment(**payment_data_default_status)
        self.assertIsInstance(payment_default.status, PaymentStatus)
        self.assertEqual(payment_default.status, PaymentStatus.EXPECTED) # Default status

        # Test with None payment_method (allowed if status is EXPECTED)
        payment_data_none_method = {
            "payment_id": 7,
            "lease_id": 107,
            "expected_amount": Decimal("300.00"),
            "status": PaymentStatus.EXPECTED, # payment_method can be None
        }
        payment_none_method = Payment(**payment_data_none_method)
        self.assertIsNone(payment_none_method.payment_method)
        self.assertIsInstance(payment_none_method.status, PaymentStatus)


if __name__ == '__main__':
    unittest.main()
