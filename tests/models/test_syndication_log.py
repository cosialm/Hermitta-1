import unittest
from datetime import datetime, timedelta
from models.syndication_log import SyndicationLog, SyndicationAction, SyndicationLogStatus

class TestSyndicationLog(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test SyndicationLog instantiation with only required fields."""
        now = datetime.utcnow()
        log = SyndicationLog(
            log_id=1,
            property_id=101,
            platform_id=1, # e.g., Property24
            action=SyndicationAction.LIST
        )

        self.assertEqual(log.log_id, 1)
        self.assertEqual(log.property_id, 101)
        self.assertEqual(log.platform_id, 1)
        self.assertEqual(log.action, SyndicationAction.LIST)
        self.assertIsInstance(log.action, SyndicationAction)

        # Check defaults
        self.assertEqual(log.status, SyndicationLogStatus.PENDING)
        self.assertIsInstance(log.status, SyndicationLogStatus)
        self.assertIsInstance(log.last_attempted_at, datetime)
        self.assertTrue((log.last_attempted_at - now).total_seconds() < 5)
        self.assertIsInstance(log.created_at, datetime)
        self.assertTrue((log.created_at - now).total_seconds() < 5) # created_at also defaults to now

        # Check other optionals are None
        self.assertIsNone(log.landlord_syndication_setting_id)
        self.assertIsNone(log.completed_at)
        self.assertIsNone(log.details)
        self.assertIsNone(log.syndication_payload_sent)
        self.assertIsNone(log.platform_response)

    def test_instantiation_with_last_attempted_at_provided(self):
        """Test that last_attempted_at uses provided value."""
        custom_attempt_time = datetime.utcnow() - timedelta(hours=1)
        log = SyndicationLog(
            log_id=2, property_id=102, platform_id=2, action=SyndicationAction.UPDATE,
            last_attempted_at=custom_attempt_time
        )
        self.assertEqual(log.last_attempted_at, custom_attempt_time)

    def test_instantiation_with_all_fields(self):
        """Test SyndicationLog instantiation with all fields provided."""
        created_ts = datetime(2023,1,1,10,0,0)
        last_attempt_ts = datetime(2023,1,1,10,5,0)
        completed_ts = datetime(2023,1,1,10,10,0)
        payload_sent_data = {"listing_id": "prop123", "title": "Beautiful Apartment"}
        platform_resp_data = {"platform_id": "XYZ789", "status": "success"}

        log = SyndicationLog(
            log_id=3,
            property_id=103,
            platform_id=3,
            action=SyndicationAction.DELIST,
            status=SyndicationLogStatus.SUCCESS,
            landlord_syndication_setting_id=501,
            last_attempted_at=last_attempt_ts,
            completed_at=completed_ts,
            details="Successfully delisted from platform.",
            syndication_payload_sent=payload_sent_data,
            platform_response=platform_resp_data,
            created_at=created_ts
        )
        self.assertEqual(log.log_id, 3)
        self.assertEqual(log.property_id, 103)
        self.assertEqual(log.action, SyndicationAction.DELIST)
        self.assertEqual(log.status, SyndicationLogStatus.SUCCESS)
        self.assertEqual(log.landlord_syndication_setting_id, 501)
        self.assertEqual(log.last_attempted_at, last_attempt_ts)
        self.assertEqual(log.completed_at, completed_ts)
        self.assertIsInstance(log.completed_at, datetime)
        self.assertEqual(log.details, "Successfully delisted from platform.")
        self.assertEqual(log.syndication_payload_sent, payload_sent_data)
        self.assertIsInstance(log.syndication_payload_sent, dict)
        self.assertEqual(log.platform_response, platform_resp_data)
        self.assertIsInstance(log.platform_response, dict)
        self.assertEqual(log.created_at, created_ts)

    def test_default_status_and_last_attempted_at(self):
        """Test default status is PENDING and last_attempted_at defaults to now."""
        now = datetime.utcnow()
        log = SyndicationLog(
            log_id=4, property_id=104, platform_id=4, action=SyndicationAction.REFRESH
        )
        self.assertEqual(log.status, SyndicationLogStatus.PENDING)
        self.assertIsInstance(log.last_attempted_at, datetime)
        self.assertTrue((log.last_attempted_at - now).total_seconds() < 5, "last_attempted_at should default to current time.")

    def test_payload_fields_handling(self):
        """Test that payload fields are None by default and can be dicts."""
        log_default = SyndicationLog(5,1,1,SyndicationAction.LIST)
        self.assertIsNone(log_default.syndication_payload_sent)
        self.assertIsNone(log_default.platform_response)

        payload = {"key":"value"}
        log_with_payloads = SyndicationLog(
            6,1,1,SyndicationAction.LIST,
            syndication_payload_sent=payload.copy(),
            platform_response=payload.copy()
        )
        self.assertEqual(log_with_payloads.syndication_payload_sent, payload)
        self.assertIsInstance(log_with_payloads.syndication_payload_sent, dict)
        self.assertEqual(log_with_payloads.platform_response, payload)
        self.assertIsInstance(log_with_payloads.platform_response, dict)


if __name__ == '__main__':
    unittest.main()
