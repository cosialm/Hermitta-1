import unittest
from datetime import datetime
from models.audit_log import (
    AuditLog, AuditActionType, AuditActionCategory, AuditActionStatus
)

class TestAuditLog(unittest.TestCase):

    def test_instantiation_with_required_fields(self):
        """Test instantiation with only required fields and default values."""
        now = datetime.utcnow()
        log = AuditLog(
            log_id=1,
            timestamp=now,
            action_type=AuditActionType.USER_LOGIN_SUCCESS
        )
        self.assertEqual(log.log_id, 1)
        self.assertEqual(log.timestamp, now)
        self.assertIsInstance(log.timestamp, datetime)
        self.assertEqual(log.action_type, AuditActionType.USER_LOGIN_SUCCESS)
        self.assertIsInstance(log.action_type, AuditActionType)

        # Check default values
        self.assertEqual(log.status, AuditActionStatus.SUCCESS)
        self.assertIsInstance(log.status, AuditActionStatus)
        self.assertIsNone(log.user_id)
        self.assertIsNone(log.target_entity_type)
        self.assertIsNone(log.target_entity_id)
        self.assertIsNone(log.details_before)
        self.assertIsNone(log.details_after)
        self.assertIsNone(log.ip_address)
        self.assertIsNone(log.user_agent)
        self.assertIsNone(log.failure_reason)
        self.assertIsNone(log.action_category)
        self.assertIsNone(log.notes)

    def test_instantiation_with_all_fields(self):
        """Test instantiation with all fields provided."""
        ts = datetime(2023, 10, 26, 10, 0, 0)
        details_b = {"key_before": "value_before"}
        details_a = {"key_after": "value_after"}

        log = AuditLog(
            log_id=2,
            timestamp=ts,
            action_type=AuditActionType.PROPERTY_UPDATED,
            user_id=101,
            target_entity_type="Property",
            target_entity_id=505, # Test with int
            details_before=details_b,
            details_after=details_a,
            ip_address="192.168.0.1",
            user_agent="TestAgent/1.0",
            status=AuditActionStatus.SUCCESS,
            failure_reason=None, # Explicitly None for SUCCESS
            action_category=AuditActionCategory.PROPERTY_MANAGEMENT,
            notes="Property rent was updated."
        )

        self.assertEqual(log.log_id, 2)
        self.assertEqual(log.timestamp, ts)
        self.assertEqual(log.action_type, AuditActionType.PROPERTY_UPDATED)
        self.assertEqual(log.user_id, 101)
        self.assertEqual(log.target_entity_type, "Property")
        self.assertEqual(log.target_entity_id, 505)
        self.assertEqual(log.details_before, details_b)
        self.assertIsInstance(log.details_before, dict)
        self.assertEqual(log.details_after, details_a)
        self.assertIsInstance(log.details_after, dict)
        self.assertEqual(log.ip_address, "192.168.0.1")
        self.assertEqual(log.user_agent, "TestAgent/1.0")
        self.assertEqual(log.status, AuditActionStatus.SUCCESS)
        self.assertIsNone(log.failure_reason)
        self.assertEqual(log.action_category, AuditActionCategory.PROPERTY_MANAGEMENT)
        self.assertIsInstance(log.action_category, AuditActionCategory)
        self.assertEqual(log.notes, "Property rent was updated.")

    def test_instantiation_with_failure_status(self):
        """Test instantiation when status is FAILURE."""
        ts = datetime.utcnow()
        log = AuditLog(
            log_id=3,
            timestamp=ts,
            action_type=AuditActionType.USER_LOGIN_FAILURE,
            user_id=None, # User might not be identified yet
            ip_address="203.0.113.10",
            status=AuditActionStatus.FAILURE,
            failure_reason="Invalid credentials provided.",
            action_category=AuditActionCategory.AUTHENTICATION
        )
        self.assertEqual(log.log_id, 3)
        self.assertEqual(log.status, AuditActionStatus.FAILURE)
        self.assertIsInstance(log.status, AuditActionStatus)
        self.assertEqual(log.failure_reason, "Invalid credentials provided.")
        self.assertEqual(log.action_category, AuditActionCategory.AUTHENTICATION)

    def test_target_entity_id_types(self):
        """Test target_entity_id with int and str types."""
        ts = datetime.utcnow()
        log_int_id = AuditLog(
            log_id=4, timestamp=ts, action_type=AuditActionType.LEASE_CREATED,
            target_entity_id=1001
        )
        self.assertEqual(log_int_id.target_entity_id, 1001)
        self.assertIsInstance(log_int_id.target_entity_id, int)

        log_str_id = AuditLog(
            log_id=5, timestamp=ts, action_type=AuditActionType.DOCUMENT_UPLOADED,
            target_entity_id="doc_abc_123"
        )
        self.assertEqual(log_str_id.target_entity_id, "doc_abc_123")
        self.assertIsInstance(log_str_id.target_entity_id, str)

    def test_enum_field_validity(self):
        """Test that enum fields are instances of their respective Enum types."""
        ts = datetime.utcnow()
        log = AuditLog(
            log_id=6,
            timestamp=ts,
            action_type=AuditActionType.MAINTENANCE_REQUEST_CREATED,
            status=AuditActionStatus.PENDING,
            action_category=AuditActionCategory.MAINTENANCE_MANAGEMENT
        )
        self.assertIsInstance(log.action_type, AuditActionType)
        self.assertIsInstance(log.status, AuditActionStatus)
        self.assertIsInstance(log.action_category, AuditActionCategory)

if __name__ == '__main__':
    unittest.main()
