import unittest
from datetime import datetime
from decimal import Decimal
from models.gateway_transaction import (
    GatewayTransaction, GatewayTransactionStatus, GatewayType
)

class TestGatewayTransaction(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test GatewayTransaction instantiation with only required fields."""
        now = datetime.utcnow()
        amount_decimal = Decimal("1000.00")

        gtx = GatewayTransaction(
            transaction_id=1,
            payment_id=101, # FK to internal Payment model
            gateway_type=GatewayType.MPESA_STK_PUSH, # Assuming MPESA_STK_PUSH is a valid GatewayType enum member
            amount=amount_decimal,
            currency="KES"
        )

        self.assertEqual(gtx.transaction_id, 1)
        self.assertEqual(gtx.payment_id, 101)
        self.assertEqual(gtx.gateway_type, GatewayType.MPESA_STK_PUSH)
        self.assertIsInstance(gtx.gateway_type, GatewayType)
        self.assertEqual(gtx.amount, amount_decimal)
        self.assertIsInstance(gtx.amount, Decimal)
        self.assertEqual(gtx.currency, "KES")

        # Check defaults
        self.assertEqual(gtx.status, GatewayTransactionStatus.PENDING)
        self.assertIsInstance(gtx.status, GatewayTransactionStatus)
        self.assertIsInstance(gtx.initiated_at, datetime) # Changed from created_at
        self.assertIsInstance(gtx.last_updated_at, datetime) # Changed from updated_at
        # Timestamps are defaulted by SQLAlchemy, direct comparison of 'now' might be tricky
        # due to minor time differences in execution. Check they are datetimes.
        self.assertIsInstance(gtx.initiated_at, datetime)
        self.assertIsInstance(gtx.last_updated_at, datetime)

        # Check other optionals are None
        self.assertIsNone(gtx.gateway_specific_transaction_id)
        self.assertIsNone(gtx.internal_merchant_ref)
        self.assertIsNone(gtx.payment_method_detail)
        self.assertIsNone(gtx.raw_request_payload)
        self.assertIsNone(gtx.raw_response_payload)
        self.assertIsNone(gtx.callback_payload)
        self.assertIsNone(gtx.error_code)
        self.assertIsNone(gtx.error_message)
        self.assertIsNone(gtx.notes)

    def test_instantiation_with_all_fields(self):
        """Test GatewayTransaction instantiation with all fields provided."""
        created_ts = datetime(2023, 1, 1, 10, 0, 0)
        updated_ts = datetime(2023, 1, 1, 11, 0, 0)
        request_p = {"data": "request_data"}
        response_p = {"data": "response_data"}
        callback_p = {"data": "callback_data"}

        gtx = GatewayTransaction(
            transaction_id=2,
            payment_id=102,
            gateway_type=GatewayType.PESAPAL, # Assuming PESAPAL is a valid GatewayType enum member
            gateway_specific_transaction_id="PESAPAL_REF_XYZ",
            internal_merchant_ref="MERCHANT_REF_ABC",
            status=GatewayTransactionStatus.SUCCESSFUL,
            amount=Decimal("50.25"),
            currency="USD",
            payment_method_detail="VISA",
            raw_request_payload=request_p,
            raw_response_payload=response_p,
            callback_payload=callback_p,
            error_code="00", # Assuming success code
            error_message="Transaction successful",
            notes="Test transaction for Pesapal.",
            initiated_at=created_ts, # Renamed from created_at
            last_updated_at=updated_ts # Renamed from updated_at
        )

        self.assertEqual(gtx.transaction_id, 2)
        self.assertEqual(gtx.payment_id, 102)
        self.assertEqual(gtx.gateway_type, GatewayType.PESAPAL)
        self.assertEqual(gtx.gateway_specific_transaction_id, "PESAPAL_REF_XYZ")
        self.assertEqual(gtx.internal_merchant_ref, "MERCHANT_REF_ABC")
        self.assertEqual(gtx.status, GatewayTransactionStatus.SUCCESSFUL)
        self.assertEqual(gtx.amount, Decimal("50.25"))
        self.assertEqual(gtx.currency, "USD")
        self.assertEqual(gtx.payment_method_detail, "VISA")
        self.assertEqual(gtx.raw_request_payload, request_p)
        self.assertIsInstance(gtx.raw_request_payload, dict)
        self.assertEqual(gtx.raw_response_payload, response_p)
        self.assertIsInstance(gtx.raw_response_payload, dict)
        self.assertEqual(gtx.callback_payload, callback_p)
        self.assertIsInstance(gtx.callback_payload, dict)
        self.assertEqual(gtx.error_code, "00")
        self.assertEqual(gtx.error_message, "Transaction successful")
        self.assertEqual(gtx.notes, "Test transaction for Pesapal.")
        self.assertEqual(gtx.initiated_at, created_ts)
        self.assertEqual(gtx.last_updated_at, updated_ts)

    def test_enum_and_decimal_types(self):
        """Test enum and decimal types are correctly handled."""
        gtx = GatewayTransaction(
            transaction_id=3, payment_id=103, gateway_type=GatewayType.STRIPE, # Assuming STRIPE is valid
            amount=Decimal("123.45"), currency="EUR",
            status=GatewayTransactionStatus.FAILED
        )
        self.assertIsInstance(gtx.gateway_type, GatewayType)
        self.assertIsInstance(gtx.status, GatewayTransactionStatus)
        self.assertIsInstance(gtx.amount, Decimal)

    def test_default_status_is_pending(self):
        """Test that the default status is PENDING."""
        gtx = GatewayTransaction(
            transaction_id=4, payment_id=104, gateway_type=GatewayType.FLUTTERWAVE, # Assuming FLUTTERWAVE is valid
            amount=Decimal("10.00"), currency="KES"
        )
        self.assertEqual(gtx.status, GatewayTransactionStatus.PENDING)

    def test_payload_fields_can_be_none_or_dict(self):
        """Test that payload fields are None by default and can be dicts."""
        gtx_default = GatewayTransaction(
            transaction_id=5, payment_id=105, gateway_type=GatewayType.OTHER_GENERIC_GATEWAY,
            amount=Decimal("1.00"), currency="KES"
        )
        self.assertIsNone(gtx_default.raw_request_payload)
        self.assertIsNone(gtx_default.raw_response_payload)
        self.assertIsNone(gtx_default.callback_payload)

        payload = {"key": "value"}
        gtx_with_payloads = GatewayTransaction(
            transaction_id=6, payment_id=106, gateway_type=GatewayType.MPESA_STK_PUSH, # Assuming MPESA_STK_PUSH is valid
            amount=Decimal("2.00"), currency="KES",
            raw_request_payload=payload.copy(),
            raw_response_payload=payload.copy(),
            callback_payload=payload.copy()
        )
        self.assertEqual(gtx_with_payloads.raw_request_payload, payload)
        self.assertIsInstance(gtx_with_payloads.raw_request_payload, dict)
        self.assertEqual(gtx_with_payloads.raw_response_payload, payload)
        self.assertIsInstance(gtx_with_payloads.raw_response_payload, dict)
        self.assertEqual(gtx_with_payloads.callback_payload, payload)
        self.assertIsInstance(gtx_with_payloads.callback_payload, dict)

if __name__ == '__main__':
    unittest.main()
