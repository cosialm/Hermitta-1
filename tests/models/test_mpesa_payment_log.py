import unittest
from datetime import datetime
from decimal import Decimal
from models.mpesa_payment_log import MpesaPaymentLog, MpesaLogStatus

class TestMpesaPaymentLog(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test MpesaPaymentLog instantiation with only required fields."""
        now = datetime.utcnow()
        amount_req = Decimal("1500.00")

        log = MpesaPaymentLog(
            log_id=1,
            lease_id=101,
            tenant_id=201,
            amount_requested=amount_req,
            phone_number_stk_pushed_to="254712345678",
            merchant_request_id="MERCH_REQ_001"
        )

        self.assertEqual(log.log_id, 1)
        self.assertEqual(log.lease_id, 101)
        self.assertEqual(log.tenant_id, 201)
        self.assertEqual(log.amount_requested, amount_req)
        self.assertIsInstance(log.amount_requested, Decimal)
        self.assertEqual(log.phone_number_stk_pushed_to, "254712345678")
        self.assertEqual(log.merchant_request_id, "MERCH_REQ_001")

        # Check defaults
        self.assertEqual(log.status, MpesaLogStatus.PENDING_STK_PUSH)
        self.assertIsInstance(log.status, MpesaLogStatus)
        self.assertIsInstance(log.created_at, datetime)
        self.assertIsInstance(log.updated_at, datetime)
        self.assertTrue((log.created_at - now).total_seconds() < 5)
        self.assertTrue((log.updated_at - now).total_seconds() < 5)

        # Check other optionals are None
        self.assertIsNone(log.checkout_request_id)
        self.assertIsNone(log.payment_id)
        self.assertIsNone(log.amount_paid)
        self.assertIsNone(log.mpesa_receipt_number)
        self.assertIsNone(log.transaction_date)
        self.assertIsNone(log.stk_push_response_payload)
        self.assertIsNone(log.stk_failure_reason)
        self.assertIsNone(log.callback_payload)
        self.assertIsNone(log.query_api_response_payload)

    def test_instantiation_with_all_fields(self):
        """Test MpesaPaymentLog instantiation with all fields provided."""
        created_ts = datetime(2023,1,1,10,0,0)
        updated_ts = datetime(2023,1,1,11,0,0)
        tx_date = datetime(2023,1,1,10,5,0) # Mpesa transaction timestamp
        stk_resp_payload = {"ResponseCode": "0", "ResponseDescription": "Success"}
        cb_payload = {"Body": {"stkCallback": {"ResultCode": 0}}}
        query_payload = {"ResponseCode": "0", "ResultDesc": "The service request is processed successfully."}

        log = MpesaPaymentLog(
            log_id=2, lease_id=102, tenant_id=202,
            amount_requested=Decimal("2000.00"),
            phone_number_stk_pushed_to="254722000111",
            merchant_request_id="MERCH_REQ_002",
            checkout_request_id="ws_CO_DMZ_12345_280220231010101010",
            payment_id=301, # FK to Payment
            amount_paid=Decimal("2000.00"),
            mpesa_receipt_number="RBA123XYZ0",
            transaction_date=tx_date,
            status=MpesaLogStatus.PAYMENT_CONFIRMED_CALLBACK,
            stk_push_response_payload=stk_resp_payload,
            stk_failure_reason=None, # Explicitly None for success case
            callback_payload=cb_payload,
            query_api_response_payload=query_payload,
            created_at=created_ts,
            updated_at=updated_ts
        )

        self.assertEqual(log.log_id, 2)
        self.assertEqual(log.lease_id, 102)
        # ... (check all other fields)
        self.assertEqual(log.checkout_request_id, "ws_CO_DMZ_12345_280220231010101010")
        self.assertEqual(log.payment_id, 301)
        self.assertEqual(log.amount_paid, Decimal("2000.00"))
        self.assertIsInstance(log.amount_paid, Decimal)
        self.assertEqual(log.mpesa_receipt_number, "RBA123XYZ0")
        self.assertEqual(log.transaction_date, tx_date)
        self.assertIsInstance(log.transaction_date, datetime)
        self.assertEqual(log.status, MpesaLogStatus.PAYMENT_CONFIRMED_CALLBACK)
        self.assertEqual(log.stk_push_response_payload, stk_resp_payload)
        self.assertIsInstance(log.stk_push_response_payload, dict)
        self.assertIsNone(log.stk_failure_reason)
        self.assertEqual(log.callback_payload, cb_payload)
        self.assertIsInstance(log.callback_payload, dict)
        self.assertEqual(log.query_api_response_payload, query_payload)
        self.assertIsInstance(log.query_api_response_payload, dict)
        self.assertEqual(log.created_at, created_ts)
        self.assertEqual(log.updated_at, updated_ts)


    def test_default_status_and_types(self):
        """Test default status and various field types."""
        log = MpesaPaymentLog(
            log_id=3, lease_id=103, tenant_id=203,
            amount_requested=Decimal("50.00"),
            phone_number_stk_pushed_to="254700000000",
            merchant_request_id="MERCH_REQ_003"
        )
        self.assertEqual(log.status, MpesaLogStatus.PENDING_STK_PUSH)
        self.assertIsInstance(log.status, MpesaLogStatus)
        self.assertIsInstance(log.amount_requested, Decimal)
        self.assertIsInstance(log.created_at, datetime)

        log.amount_paid = Decimal("50.00")
        self.assertIsInstance(log.amount_paid, Decimal)
        log.transaction_date = datetime.utcnow()
        self.assertIsInstance(log.transaction_date, datetime)


    def test_stk_failure_case(self):
        """Test a scenario where STK push fails immediately."""
        stk_fail_payload = {"ResponseCode": "1", "ResponseDescription": "Invalid Phone Number"}
        log = MpesaPaymentLog(
            log_id=4, lease_id=104, tenant_id=204,
            amount_requested=Decimal("100.00"),
            phone_number_stk_pushed_to="invalid_num",
            merchant_request_id="MERCH_REQ_004",
            status=MpesaLogStatus.STK_PUSH_FAILED,
            stk_push_response_payload=stk_fail_payload,
            stk_failure_reason="Invalid MSISDN"
        )
        self.assertEqual(log.status, MpesaLogStatus.STK_PUSH_FAILED)
        self.assertEqual(log.stk_failure_reason, "Invalid MSISDN")
        self.assertEqual(log.stk_push_response_payload, stk_fail_payload)
        self.assertIsNone(log.callback_payload) # No callback if STK push fails upfront

if __name__ == '__main__':
    unittest.main()
